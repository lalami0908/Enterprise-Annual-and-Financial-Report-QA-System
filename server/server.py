# -*- coding: UTF-8 -*-
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_restful import Api, Resource, reqparse
from functools import wraps
from datetime import datetime, timedelta
from flask import Flask, Blueprint, jsonify, request, current_app, render_template, redirect
from flask_cors import CORS
#import jwt
import json
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from werkzeug.security import generate_password_hash, check_password_hash
import os
import pusher

import torch
from transformers import BertTokenizer, BertForQuestionAnswering
from transformers import BertModel
from sentence_transformers import SentenceTransformer
from sentence_transformers import models
import numpy as np
from os import listdir
from os.path import isfile, join
from numpy import dot
from numpy.linalg import norm
import pandas as pd
from bert_qa import BertQA
import warnings
import pickle


#api = Blueprint('api', __name__)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///tmp/test.db"
app.config['JWT_SECRET_KEY'] = 'FiNanCial-Qa'  # Change this!
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False

jwt = JWTManager(app)
jwt.init_app(app)
db = SQLAlchemy(app)
CORS(app)
api = Api(app)


@app.route('/')
def index():
    return jsonify("Pong!")


@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()


def token_required(f):
    @wraps(f)
    def _verify(*args, **kwargs):
        auth_headers = request.headers.get('Authorization', '').split()

        invalid_msg = {
            'message': 'Invalid token. Registeration and / or authentication required',
            'authenticated': False
        }
        expired_msg = {
            'message': 'Expired token. Reauthentication required.',
            'authenticated': False
        }

        if len(auth_headers) != 2:
            return jsonify(invalid_msg), 401

        try:
            token = auth_headers[1]
            data = jwt.decode(token, current_app.config['SECRET_KEY'])
            user = User.query.filter_by(email=data['email']).first()
            if not user:
                raise RuntimeError('User not found')
            return f(user, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            # 401 is Unauthorized HTTP status code
            return jsonify(expired_msg), 401
        except (jwt.InvalidTokenError, Exception) as e:
            print(e)
            return jsonify(invalid_msg), 401

    return _verify


@app.route('/company', methods=["GET"])
def company():
    from models import User, Company, Record
    cl = [1229, 1301, 1762, 1773, 1776, 1907, 2002, 2105, 2201, 2301, 2303, 2308, 2312, 2330, 2353, 2357,
          2382, 2385, 2392, 2409, 2412, 2454, 2609, 2610, 2618, 2882, 2888, 2905, 3231, 3702, 5522, 9904]
    companies = [Company.query.filter_by(
        code=companyID).one() for companyID in cl]
    return jsonify([Company.to_dict(company) for company in companies]), 202


@app.route('/get_hot_company', methods=["GET"])
def get_hot_company():
    from models import User, Company, Record
    records = Record.query.add_columns(
        func.count(), Record.company_id).group_by(Record.company_id).all()

    def sortSecond(val):
        return val[1]

    def get_dict_list_from_result(result):
        list_dict = []
        for i in result:
            # i_dict = i._asdict()  # sqlalchemy.util._collections.result , has a method called _asdict()
            i_dict = dict(count=i[1], company_id=i[2])
            list_dict.append(i_dict)
        return list_dict

    records.sort(key=sortSecond, reverse=True)
    charts = get_dict_list_from_result(records)

    for chart in charts:
        company = Company.query.filter_by(
            code=chart['company_id']).first().full_name
        chart['company_name'] = company

    return jsonify([chart for chart in charts])


@app.route('/get_random_record', methods=["GET"])
def get_random_record():
    from models import User, Company, Record
    records = Record.query.order_by(func.random()).limit(5)
    return jsonify([Record.to_dict(record) for record in records]), 200


@app.route('/register', methods=["POST"])
def register():
    from models import User, Company, Record
    data = request.get_json()
    #user = User(**data)
    email = data.get("email")
    username = data.get("username")
    password = generate_password_hash(data.get("password"))

    try:
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
    except:
        return jsonify({
            "status": "error",
            "message": "Could not add user"
        })

    return jsonify({
        "status": "success",
        "message": "User added successfully"
    }), 201


@app.route('/login', methods=["POST"])
def login():
    from models import User, Company, Record
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({
            "status": "failed",
            "message": "Failed getting user"
        }), 401

    # Generate a token
    access_token = create_access_token(identity=email)

    return jsonify({
        "status": "success",
        "message": "login successful",
        "data": {
            "id": user.id,
            "email": user.email,
            "token": access_token,
            "username": user.username
        }
    }), 200

# way2
    # data = request.get_json()
    # user = User.authenticate(**data)

    # if not user:
    #     return jsonify({ 'message': 'Invalid credentials', 'authenticated': False }), 401

    # token = jwt.encode({
    #     'sub': user.email,
    #     'iat': datetime.utcnow(),
    #     'exp': datetime.utcnow() + timedelta(minutes=30)},
    #     current_app.config['SECRET_KEY'])
    # return jsonify({ 'token': token.decode('UTF-8') })


@app.route('/identity', methods=["POST"])
# @jwt_required
def protected():
    #
    identity = get_jwt_identity()
    return jsonify(logged_in_as=identity), 206


@app.route('/record', methods=["POST"])
# @jwt_required
def record():
    from models import User, Company, Record
    data = request.get_json()
    query_text = data.get("query")
    answer = data.get("answer")
    year = data.get("year")
    season = data.get("season")
    user_id = data.get("user_id")
    company_id = data.get("company_id")

    # try:
    new_record = Record(query_text=query_text, answer=answer, year=year,
                        season=season, user_id=user_id, company_id=company_id)
    db.session.add(new_record)
    db.session.commit()
    # except:
    #     return jsonify({
    #         "status": "error",
    #         "message": "Could not add record"
    #     })

    return jsonify({
        "status": "success",
        "message": "Record added successfully"
    }), 203


@app.route('/get_record', methods=["POST"])
# @jwt_required
def get_record():
    from models import User, Company, Record
    data = request.get_json()
    user_id = data.get("user_id")
    records = Record.query.filter_by(user_id=user_id).distinct(
        Record.company_id).order_by(Record.id.desc()).all()
    return jsonify([Record.company_to_dict(record) for record in records]), 202

###  ####
# @jwt_required
# @app.route('/get_company_record/<int:companyID>', methods=["POST"])


@app.route('/get_company_record', methods=["POST"])
def get_company_record():
    from models import User, Company, Record
    data = request.get_json()
    user_id = data.get("user_id")
    company_id = data.get("companyID")
    records = Record.query.filter_by(
        user_id=user_id, company_id=company_id).all()
    return jsonify([Record.to_dict(record) for record in records]), 200

###  ####


@app.route('/get_company_name', methods=["POST"])
def get_company_name():
    from models import User, Company, Record
    data = request.get_json()
    company_id = data.get("companyID")
    company = Company.query.filter_by(code=company_id).first()
    return jsonify({
        "short_name": company.short_name,
        "full_name": company.full_name
    }), 200


@app.route('/check_company_data_exist', methods=["POST"])
# @jwt_required
def check_company_data_exist():
    from models import User, Company, Record
    exist = False
    data = request.get_json()
    company = data.get("company")
    season = data.get("season")
    year = data.get("year")
    folderPath = "../jsons/" + str(company) + "/"
    txtfile = str(year) + ".json"
    csvfile = str(year) + str(season) + ".json"
    print(folderPath + txtfile)
    print(folderPath + csvfile)
    if os.path.exists(folderPath + txtfile) or os.path.exists(folderPath + csvfile):
        exist = True

    return jsonify({
        "status": "success",
        "exist": exist
    }), 202


########################### JsonBertEmbedding ############################
parser = reqparse.RequestParser()
parser.add_argument("query")
parser.add_argument("company")
parser.add_argument("season")
parser.add_argument("year")


class JsonBertEmbeddingPredict(Resource):
    def post(self):
        # query from post
        args = parser.parse_args()
        query = args["query"]
        year = args["year"]
        season = args["season"]
        company = args["company"]
        vecs = []
        sentences = []
        folderPath = "jsons/" + company + "/"
        if season is None:
            season = ''
        if year is None:
            year = ''

        txtfile = year + ".json"
        csvfile = year + season + ".json"

        if os.path.exists(folderPath + txtfile):
            with open(folderPath + txtfile) as json_file:
                data = json.load(json_file)
                for k in data:
                    vecs.append(data[k])
                    sentences.append(k)
        else:
            print("No Annual Report.")

        if os.path.exists(folderPath + csvfile):
            with open(folderPath + csvfile) as json_file:
                data = json.load(json_file)
                for k in data:
                    vecs.append(data[k])
                    sentences.append(k)
        else:
            print("No Financial Report.")
        # print("file loading finished", time.time()-starttime)
        # loading bert model for sentence embedding
        word_embedding_model = models.Transformer("./bertmodels/output4")
        # Apply mean pooling to get one fixed sized sentence vector
        pooling_model = models.Pooling(word_embedding_model.get_word_embedding_dimension(),
                                       pooling_mode_mean_tokens=True,
                                       pooling_mode_cls_token=False,
                                       pooling_mode_max_tokens=False)

        model_sentence_embedding = SentenceTransformer(
            modules=[word_embedding_model, pooling_model])

        vecs_sentence_embedding = np.array(vecs)
        vec_target_sentence_embedding = np.array(
            model_sentence_embedding.encode(query))  # Batch size 1
        similarities = []
        for vec in vecs_sentence_embedding:
            cos_sim = dot(vec_target_sentence_embedding, vec) / \
                (norm(vec_target_sentence_embedding)*norm(vec))
            similarities.append(cos_sim)
        sentences = [x for _, x in sorted(zip(similarities, sentences))]

        similarities = sorted(similarities)
        print("getContent: " + sentences[-1])
        return sentences[-1]


########################### Question Answering ###########################

QAparser = reqparse.RequestParser()
QAparser.add_argument("query")
QAparser.add_argument("context")

# warnings.filterwarnings('ignore')
tokenizer = BertTokenizer(
    vocab_file="./bertmodels/trained_model/vocab.txt", do_lower_case=True)
model = BertForQuestionAnswering.from_pretrained('./bertmodels/trained_model/')
device = 'cuda' if torch.cuda.is_available() else 'cpu'
bertQA = BertQA(model=model, tokenizer=tokenizer, device=device)


class QAPredict(Resource):
    def post(self):
        args = QAparser.parse_args()
        question = args["query"]
        context = args["context"]
        answer_results = bertQA.ask(context, question)
        # score:2.17795 start_index:11(1.07034) end_index:13(1.10761) answer:王大明
        for answer_result in answer_results:
            print("score:%3.5f start_index:%d(%3.5f) end_index:%d(%3.5f) answer:%s"
                  % (answer_result[1]+answer_result[3], answer_result[0], answer_result[1], answer_result[2], answer_result[3], answer_result[4]))
            return answer_result[4].replace("#", "")


api.add_resource(JsonBertEmbeddingPredict, "/embedding")
api.add_resource(QAPredict, "/qa")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5020, debug=True)

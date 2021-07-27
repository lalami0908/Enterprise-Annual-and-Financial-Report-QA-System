// https://github.com/vuetifyjs/vuetify/blob/master/packages/docs/src/examples/autocompletes/intermediate/asynchronous.vue
// https://vuetifyjs.com/en/components/autocompletes/
<template>
  <v-container>
    <v-main>
      <div class="chooseCompany">
        <v-card-text style="margin-top: 20px">
          <v-toolbar-title><strong>選擇公司</strong></v-toolbar-title>
          <br />

          <v-autocomplete
            v-model="selectCompany"
            :loading="loading"
            :items="items"
            :search-input.sync="search"
            item-text="name"
            item-value="code"
            loader-height="3"
            cache-items
            hide-no-data
            hide-details
            label="請輸入想要詢問的公司名稱"
            solo-inverted
            chips
            input
            @compositionstart="compositionstart($event)"
            @compositionend="compositionend($event)"
          ></v-autocomplete>

          <v-row align="center">
            <v-col class="d-flex" cols="12" sm="6">
              <v-select
                v-model="selectYear"
                :items="years"
                label="選擇年分"
                filled
              ></v-select>
            </v-col>
            <v-col class="d-flex" cols="12" sm="6">
              <v-select
                v-model="selectSeason"
                :items="seasons"
                label="選擇季"
                filled
              ></v-select>
            </v-col>
          </v-row>

          <br />
          <br />
          <br />
          <br />
          <br />
          <br />
          <br />

          <div class="text-center">
            <v-btn style="margin: 5px" @click="authenticate()">確定選擇</v-btn>
          </div>
        </v-card-text>
      </div>
    </v-main>
  </v-container>
</template>

<script>
export default {
  name: "askCompanyChoose",
  data: () => ({
    drawer: null,
    loading: false,
    years: ["2019", "2018", "2017", "2016", "2015"],
    seasons: ["Q1", "Q2", "Q3", "Q4"],
    items: [],
    search: null,
    selectCompany: null,
    selectYear: null,
    selectSeason: null,
  }),
  mounted() {
    // getCompanyNames() {
    this.axios({
      method: "get",
      url: "http://127.0.0.1:5020/company",
    })
      .then((response) => {
        this.items = response.data;

        // let i;
        // for (i = 0; i < this.items.length; i += 1) {
        //     this.items[i].name = this.items[i].full_name + this.items[i].short_name;
        // }
      })
      .catch((error) => {
        // eslint-disable-next-line
        console.log("getCompanyNames");
      });
    // },
  },

  // watch: {
  //     search(val) {
  //         if (val && val !== this.selectCompany) {
  //             this.querySelections(val);
  //         }
  //     },
  // },

  methods: {
    authenticate() {
      console.log("enter button");
      console.log(this.selectCompany);
      this.$router.push({
        path: "/query",
        query: {
          companyId: this.selectCompany,
          Year: this.selectYear,
          Season: this.selectSeason,
        },
      });
      // query 帶參數過去
      // https://router.vuejs.org/zh/guide/essentials/navigation.html
    },
  },
};
</script>


<style scoped>
.chooseCompany {
  width: 500px;
  height: 500px;
  border: 1px solid #cccccc;
  background-color: #000000;
  margin: auto;
  margin-top: 80px;
  padding: 20px;
}
.input-form {
  margin-bottom: 9px;
}
</style>

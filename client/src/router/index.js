import Vue from 'vue';
import VueRouter from 'vue-router';
import $ from 'jquery';
import Home from '../views/Home.vue';
import About from '../views/About.vue';
import Chat from '../components/chat.vue';
import Login from '../components/Login.vue';
import AskCompanyChoose from '../components/AskCompanyChoose.vue';
import GetRecord from '../components/GetRecord.vue';
import GetRecordCompany from '../components/GetRecordCompany.vue';


Vue.use(VueRouter);

const routes = [{
        path: '/',
        name: 'Home',
        component: Home,
    },
    {
        path: '/about',
        name: 'About',
        // component: About,
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: About,
    },



    {
        path: '/login',
        name: 'Login',
        component: Login,
        props: true,
    },
    {
        path: '/askCompanyChoose',
        name: 'AskCompanyChoose',
        component: AskCompanyChoose,
        props: true,
    },

    {
        path: '/query',
        name: 'Chat',
        component: Chat,
        props: true,
    },

    {
        path: '/historyCompanyChoose',
        name: 'GetRecord',
        component: GetRecord,
        props: true,
    },

    {
        path: '/history',
        name: 'GetRecordCompany',
        component: GetRecordCompany,
        props: true,
    },

    {
        path: '/feedback',
        name: 'AskCompanyChoose',
        component: AskCompanyChoose,
        props: true,
    },
];

const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes,
});

export default router;

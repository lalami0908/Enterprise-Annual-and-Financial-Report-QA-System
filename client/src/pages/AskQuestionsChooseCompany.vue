// https://github.com/vuetifyjs/vuetify/blob/master/packages/docs/src/examples/autocompletes/intermediate/asynchronous.vue
// https://vuetifyjs.com/en/components/autocompletes/
<template>
<form>
<v-select 
    v-model="selectYear"
    v-bind="$attrs"
    :items="years"
    label="選擇年分"
></v-select>
</form>
</template>

<script>

export default {
    name: 'askQuestionsChooseCompany',
    data: () => ({
        drawer: null,
        loading: false,
        years: ['2019', '2018', '2017', '2016', '2015'],
        seasons: ['Q1', 'Q2', 'Q3', 'Q4'],
        items: [],
        search: null,
        selectCompany: null,
        selectYear: null,
        selectSeason: null,
    }),
    mounted() {
        // getCompanyNames() {
            this.axios({
                method: 'get',
                url: 'http://127.0.0.1:5020/company',
            }).then((response) => {
                this.items = response.data;
                console.log(this.items);
            }).catch((error) => {
                // eslint-disable-next-line
                console.log('getCompanyNames');
            });
        // },
    },
    methods: {
        authenticate() {
            console.log('enter button');
            console.log(this.selectCompany);
            this.axios({
                method: 'post',
                url: 'http://127.0.0.1:5020/check_company_data_exist',
                data: {
                    year: this.selectYear,
                    season: this.selectSeason,
                    company: this.selectCompany,
                },
            })
                .then((response) => {
                    alert(response);

            }


           // this.$router.push({ path: '/query', query: { companyId: this.selectCompany, Year: this.selectYear, Season: this.selectSeason } });
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

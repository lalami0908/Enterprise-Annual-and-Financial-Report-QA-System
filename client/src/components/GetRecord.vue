<template>
  <v-container>
    <v-main>
      <div class="chooseCompany">
        <v-card-text style="margin-top: 20px">
          <v-toolbar-title><strong>查詢記錄：選擇公司</strong></v-toolbar-title>
          <br />

          <v-autocomplete
            v-model="selectCompany"
            :loading="loading"
            :items="Companies"
            :search-input.sync="search"
            item-text="company_name"
            item-value="company_id"
            loader-height="3"
            hide-no-data
            hide-details
            label="請輸入想要查尋紀錄的公司"
            solo-inverted
            chips
            input
          ></v-autocomplete>

          <br />
          <br />
          <br />
          <br />
          <br />
          <br />
          <br />
          <br />
          <br />
          <br />
          <br />

          <div class="text-center">
            <v-btn style="margin: 5px" @click="getCompanyRecord()"
              >確定選擇</v-btn
            >
          </div>
        </v-card-text>
      </div>
    </v-main>
  </v-container>
</template>


<script>
export default {
  name: "GetRecord",
  data: () => ({
    selectCompany: null,
    Companies: [],
  }),
  mounted() {
    this.axios({
      method: "post",
      url: "http://127.0.0.1:5020/get_record",
      data: { user_id: 2 },
    })
      .then((response) => {
        this.Companies = response.data;
      })
      .catch((error) => {
        // eslint-disable-next-line
        console.log("error");
      });
  },

  methods: {
    getCompanyRecord() {
      this.$router.push({
        path: "/history",
        query: { companyId: this.selectCompany },
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

<template>
  <div id="app">
    <Chat
      iconColorProp="#e6e6e6"
      messageOutColorProp="#4d9e93"
      messageInColorProp="#f1f0f0"
      :messageListProp="messageList"
      :initOpenProp="initOpen"
      @onToggleOpen="handleToggleOpen"
      @onMessageWasSent="handleMessageReceived"
    />
  </div>
</template>

<script>
import Chat from "./ChatWidget.vue";

export default {
  name: "chat",
  components: {
    Chat,
  },
  data: () => ({
    messageList: [],
    initOpen: true,
    toggledOpen: false,
  }),
  // 剛在入頁面就會執行 看一下有沒有正確帶參數(其實url也會掛Q)
  mounted() {
    console.log("=============== test params ==============");
    console.log(this.$route.query.companyId);
    console.log(this.$route.query.Year);
    console.log(this.$route.query.Season);
    console.log("=============== test params ==============");
    this.messageList.push({ body: "歡迎提出您的問題", author: "them" });
  },
  methods: {
    // Send message from you
    // addRecord(query, answer, year, season, userId, companyId) {
    //     console.log('test');
    // },
    // 送出訊息 要調成跟JsonBerting要得參數
    handleMessageReceived(message) {
      this.messageList.push(message);
      let cxt = "";
      this.axios({
        method: "post",
        url: "http://127.0.0.1:5020/embedding",
        data: {
          query: message.body,
          year: this.$route.query.Year,
          season: this.$route.query.Season,
          company: this.$route.query.companyId,
        },
      })
        .then((response) => {
          cxt = response.data;
          this.axios({
            method: "post",
            url: "http://127.0.0.1:5020/qa",
            data: { query: message.body, context: cxt },
          })
            .then((res) => {
              this.messageList.push({ body: res.data, author: "them" });
              // addRecord(message, res.data, this.$route.query.Year, this.$route.query.Season, 123, this.$route.query.companyId);
            })
            .catch((error) => {
              // eslint-disable-next-line
              console.log(error);
            });
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
        });
      // this.axios({
      //             method: 'post',
      //             url: 'http://127.0.0.1:5050/qa',
      //             data: { query: message, context: cxt },
      // })
      //     .then((res) => {
      //         console.log(res);
      //         this.messageList.push({ body: res.data, author: 'them' });
      //     })
      //     .catch((error) => {
      //         // eslint-disable-next-line
      //         console.log(error);
      //     });
    },
    // Receive message from them (handled by you with your backend)
    handleMessageResponse(message) {
      if (message.length > 0) {
        this.messageList.push({ body: "嗨~~~", author: "them" });
      }
    },
    // Chat toggled open event emitted
    handleToggleOpen(open) {
      this.toggledOpen = open;
      // connect/disconnect websocket or something
    },
    // Audible chat response noise, use whatever noise you want
  },
  // init chat with a message
  watch: {
    messageList(newList) {
      const nextMessage = newList[newList.length - 1];
      const isIncoming = (nextMessage || {}).author !== "you";
      if (isIncoming && this.toggledOpen) {
        this.handleMessageResponseSound();
      }
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>

<template>
  <div>
    <v-app>
    <v-navigation-drawer
      v-model="drawer"
      app
      clipped
    >
      <v-list dense>
        <v-list-item
            v-for="item in items"
            :key="item.title"
            :to="item.link"
            link
        >
          <v-list-item-icon>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title>{{ item.title }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

      </v-list>

    </v-navigation-drawer>
    <v-app-bar
      app
      dark
      clipped-left
    >
      <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
      <v-toolbar-title>歡迎來到年報QA系統</v-toolbar-title>
    </v-app-bar>
    <!-- <Login />
      <NavBar :logged_user="logged_user_username" /> -->
    <router-view/>
    <v-footer
      app
    >
      <span class="white--text">&copy; {{ new Date().getFullYear() }}</span>
    </v-footer>
  </v-app>
 </div>
</template>

<script>

  export default {
    name: 'app',
    data: () => ({
      drawer: null,
      items: [
        { title: '登入', icon: 'mdi-account', link: '/login' },
        { title: '關於我們', icon: 'mdi-home', link: '/' },
        { title: '提出查詢', icon: 'mdi-view-dashboard', link: '/askCompanyChoose' },
        { title: '歷史詢問', icon: 'mdi-image', link: '/historyCompanyChoose' },
        { title: '大家都在問', icon: 'mdi-help-box', link: '/leaderboard' },
        { title: '意見回饋', icon: 'mdi-cog', link: '/feedback' },
      ],
    }),
    created() {
      this.$vuetify.theme.dark = true;
      // this.$vuetify.theme.themes.light.primary = '#4caf50';
    },
  };
</script>

<style>

</style>

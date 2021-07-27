<template>
  <div>
    <v-main id="test">
      <v-container
        class="fill-height"
        fluid
      >
        <v-row
          align="center"
          justify="center"
          class="text-center"
        >
        <v-col cols="12"></v-col>

        <v-col cols="12">
          <v-img
            :src="require('../assets/logo.svg')"
            class="my-3"
            contain
            height="200"
          />
        </v-col>

        <v-col class="mb-4">
          <h1 class="display-2 font-weight-bold mb-3">
            Welcome
          </h1>
        </v-col>

        <v-col
          class="mb-5"
          cols="12"
        >
          <h2 class="headline font-weight-bold mb-3">
            What's next?
          </h2>

          <v-row justify="center">
            <a
              v-for="(next, i) in whatsNext"
              :key="i"
              :href="next.href"
              class="subheading mx-3"
              target="_blank"
            >
              {{ next.text }}
            </a>
          </v-row>
        </v-col>
      </v-row>
      </v-container>
    </v-main>
  </div>
</template>

<script>
  export default {
    name: 'HelloWorld',
    data: () => ({

      drawer: null,

      whatsNext: [
        {
          text: 'Explore components',
          href: 'https://vuetifyjs.com/components/api-explorer',
        },
        {
          text: 'Select a layout',
          href: 'https://vuetifyjs.com/getting-started/pre-made-layouts',
        },
      ],
    }),
    created() {
      this.$vuetify.theme.dark = true;
    },
  };
</script>

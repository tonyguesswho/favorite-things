<template>
  <div class="card my-3">
    <div class="card-header d-flex justify-content-between">
      <span> Category: {{ favorite.category.name }} </span>
      <span class="title">
        {{ favorite.title.charAt(0).toUpperCase() + favorite.title.slice(1) }}
      </span>
      <span> Rank: {{ favorite.ranking }} </span>
    </div>
    <div class="card-body">
      <div class="my-2" v-html="favorite.description.substring(0, 200)"></div>
      <div class="d-flex justify-content-between">
        <router-link
          :to="`/favorite/${favorite.id}`"
          class="btn btn-outline-info btn-sm"
        >
          More Details
        </router-link>
        <div>
          <i class="fas fa-trash mr-2 link" @click="handleDelete"></i>
          <router-link :to="`/favorite/${favorite.id}/edit`" class="link">
            <i class="fas fa-pen"></i>
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>
<style>
.link {
  color: black;
  cursor: pointer;
}
.link:hover {
  color: #34a8eb;
}
.title {
  font-weight: bold;
}
</style>

<script>
export default {
  methods: {
    handleDelete() {
      this.$emit("delete");
    }
  },
  props: ["favorite"]
};
</script>

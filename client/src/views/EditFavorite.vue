<template>
  <div class="container">
    <div class="row">
      <div class="col-md-8 offset-md-2">
        <div class="card my-5">
          <div class="card-body">
            <div class="form-group">
              <label>Title</label>
              <input
                type="text"
                placeholder="Descriptive Name"
                class="form-control mb-3"
                v-model="title"
                required
                :class="{
                  'is-invalid': errors.title,
                  'is-valid': submitted && !errors.title
                }"
              />
              <p class="errors" v-if="errors.title">
                <small
                  class="text-danger"
                  v-for="error in errors.title"
                  :key="error"
                  >{{ error }}</small
                >
              </p>
            </div>
            <div class="form-group shadow-textarea">
              <label for="description">Description</label>
              <textarea
                class="form-control z-depth-1"
                id="description"
                rows="3"
                placeholder="Enter Description..."
                v-model="description"
              ></textarea>
            </div>
            <div class="errors" v-if="errors.description">
              <small
                class="text-danger"
                v-for="error in errors.description"
                :key="error"
                >{{ error }}</small
              >
            </div>
            <div class="form-row">
              <div class="col-md-5">
                <label for="">Rank</label>
                <input
                  type="number"
                  placeholder="Enter Rank"
                  class="form-control"
                  v-model="ranking"
                  :class="{
                    'is-invalid': errors.ranking,
                    'is-valid': submitted && !errors.ranking
                  }"
                />
                <div class="errors" v-if="errors.ranking">
                  <small
                    class="text-danger"
                    v-for="error in errors.ranking"
                    :key="error"
                    >{{ error }}</small
                  >
                </div>
              </div>
            </div>
            <div v-if="Object.keys(metadata).length > 0" class="my-2 card">
              <p class="card-header text-center">MetaData</p>
              <div class="card-body">
                <p
                  v-for="(info, key) in metadata"
                  :key="info"
                  class="d-flex justify-content-between"
                >
                  <span>{{ key }} </span>
                  <span>{{ info }}</span>
                  <button
                    class="btn btn-outline-danger btn-sm"
                    @click="$delete(metadata, key)"
                  >
                    Delete
                  </button>
                </p>
              </div>
            </div>
            <div class="form-row my-4" v-if="dataType != 'select'">
              <div class="errors" v-if="metaError">
                <small class="text-danger">{{ metaError }}</small>
              </div>
              <div class="col-md-4">
                <input
                  type="text"
                  placeholder="Enter Field Name"
                  class="form-control required"
                  v-model="metaKey"
                />
              </div>
              <div class="col-md-5 mr-3">
                <input
                  :type="dataType"
                  :placeholder="`Enter ${dataType}`"
                  class="form-control"
                  v-model="metaValue"
                />
              </div>
              <button
                class="btn btn-outline-success btn-sm mr-3"
                @click="addMetaData"
              >
                Add
              </button>
              <button
                class="btn btn-outline-danger btn-sm ml-4"
                @click="closeMetaForm"
              >
                Close
              </button>
            </div>
            <div class="d-flex justify-content-center">
              <p class="my-4 mr-5">Add More Information</p>
              <select name="" id="" class="my-3" v-model="dataType">
                <option value="select">Select data Type</option>
                <option value="text">Text</option>
                <option value="number">Number</option>
                <option value="date">Date</option>
              </select>
            </div>
            <div class="d-flex justify-content-center">
              <button class="btn btn-success mt-3 mr-2" @click="editFav">
                Update
              </button>
              <button
                class="btn btn-outline-success mt-3 ml-2"
                @click="$router.go(-1)"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Axios from "axios";
export default {
  beforeRouteEnter(to, from, next) {
    if (localStorage.getItem("token")) {
      return next();
    } else {
      return next({ path: "/login" });
    }
  },

  mounted() {
    this.getDetails();
  },
  data() {
    return {
      favorite: {},
      errors: {},
      loading: true,
      description: "",
      title: "",
      ranking: null,
      categoryId: "",
      submitted: false,
      category: "",
      metadata: {},
      dataType: "select",
      metaKey: "",
      metaValue: "",
      metaError: ""
    };
  },

  methods: {
    async getDetails() {
      try {
        this.loading = true;
        const favorite = await Axios.get(
          `${process.env.VUE_APP_API_URL}/api/favorite/favorites/${
            this.$route.params.id
          }/`,
          { headers: { Authorization: `Token ${this.$root.authToken}` } }
        );
        this.title = favorite.data.favorite.title;
        this.description = favorite.data.favorite.description;
        this.ranking = favorite.data.favorite.ranking;
        this.metadata = favorite.data.favorite.metadata;
        this.categoryId = favorite.data.favorite.category.id;
        this.loading = false;
      } catch (error) {
        this.errors = error.response.data.errors;
      }
    },
    async editFav() {
      try {
        await Axios.put(
          `${process.env.VUE_APP_API_URL}/api/favorite/favorites/${
            this.$route.params.id
          }/`,
          {
            title: this.title,
            description: this.description,
            categoryId: parseInt(this.categoryId),
            ranking: parseInt(this.ranking),
            metadata: this.metadata
          },
          { headers: { Authorization: `Token ${this.$root.authToken}` } }
        );
        this.submitted = true;
        this.$noty.success("Updated Favorite Thing Successfully");
        this.$router.go(-1);
      } catch (error) {
        this.errors = error.response.data.errors;
        this.$noty.error("Oops Something went wrong");
        this.submitted = true;
      }
    }
  },
  addMetaData() {
    if (!this.metaKey || !this.metaValue) {
      this.metaError = "Metadata field is required";
    } else {
      this.metadata[this.metaKey] = this.metaValue;
      this.dataType = "select";
      this.metaError = "";
      this.metaValue = "";
      this.metaKey = "";
    }
  },
  closeMetaForm() {
    this.dataType = "select";
    this.metaError = "";
  }
};
</script>

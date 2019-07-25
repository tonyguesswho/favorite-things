<template>
  <div class="container">
    <div class="row">
      <div class="col-md-8 offset-md-2">
        <div class="loader text-center">
          <i class="fas fa-spin fa-5x fa-spinner" v-if="loading"></i>
        </div>
        <div class="card my-5" v-if="!loading">
          <div class="errors mr-6" v-if="metaError">
            <small class="text-danger">{{ metaError }}</small>
          </div>
          <div class="card-body">
            <div class="form-group">
              <label>Title</label>
              <input
                type="text"
                placeholder="Enter title"
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
              <div class="col-md-6">
                <select
                  class="form-control"
                  v-model="categoryId"
                  :class="{
                    'is-invalid': errors.categoryId,
                    'is-valid': submitted && !errors.categoryId
                  }"
                >
                  <option>Select a Category</option>
                  <option
                    :value="category.id"
                    v-for="category in categories"
                    :key="category.id"
                  >
                    {{ category.name }}
                  </option>
                </select>
                <div class="errors" v-if="errors.categoryId">
                  <small
                    class="text-danger"
                    v-for="error in errors.categoryId"
                    :key="error"
                    >{{ error }}</small
                  >
                </div>
              </div>
              <i
                class="fas fa-2x fa-plus col-md-1"
                data-toggle="modal"
                data-target="#myModal"
              ></i>
              <div class="col-md-5">
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
            <div class="text-center">
              <button class="btn btn-success mt-3 btn-lg" @click="createFav">
                Save
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <!-- The Modal -->
    <div class="modal" id="myModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h4 class="modal-title">Add New Category</h4>
            <button type="button" class="close" data-dismiss="modal">
              &times;
            </button>
          </div>

          <div class="modal-body">
            <input
              type="text"
              placeholder="Name"
              class="form-control"
              v-model="category"
            />
          </div>
          <div class="errors" v-if="errors.name">
            <small
              class="text-danger"
              v-for="error in errors.name"
              :key="error"
              >{{ error }}</small
            >
          </div>

          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-success"
              @click="createCategory"
            >
              Save
            </button>
            <button
              type="button"
              class="btn btn-danger"
              data-dismiss="modal"
              @click="errors = {}"
            >
              Close
            </button>
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
    this.getCategories();
  },

  data() {
    return {
      description: "",
      title: "",
      categories: [],
      ranking: null,
      errors: {},
      categoryId: "Select a Category",
      submitted: false,
      category: "",
      metadata: {},
      dataType: "select",
      metaKey: "",
      metaValue: "",
      metaError: "",
      loading: false
    };
  },
  methods: {
    async createFav() {
      try {
        this.loading = true;
        await Axios.post(
          `${process.env.VUE_APP_API_URL}/api/favorite/favorites/`,
          {
            title: this.title,
            description: this.description.trim(),
            categoryId: parseInt(this.categoryId),
            ranking: parseInt(this.ranking),
            metadata: this.metadata
          },
          { headers: { Authorization: `Token ${this.$root.authToken}` } }
        );
        this.loading = false;
        this.submitted = true;
        this.$noty.success("Created Favorite Thing Successfully");
        this.$router.push("/favorites");
      } catch (error) {
        this.errors = error.response.data.errors;
        this.$noty.error("Oops Something went wrong");
        this.loading = false;
        this.submitted = true;
      }
    },

    async getCategories() {
      try {
        const response = await Axios.get(
          `${process.env.VUE_APP_API_URL}/api/category/categories/`,
          { headers: { Authorization: `Token ${this.$root.authToken}` } }
        );
        this.categories = response.data;
      } catch (error) {
        this.$noty.error("An error occurred");
      }
    },
    async createCategory() {
      try {
        const response = await Axios.post(
          `${process.env.VUE_APP_API_URL}/api/category/categories/`,
          { name: this.category },
          { headers: { Authorization: `Token ${this.$root.authToken}` } }
        );
        this.categoryId = response.data.id;
        this.errors = {};
        await this.getCategories();
        this.$noty.success(" Category Created Successfully");
        $("#myModal").modal("hide");
      } catch (error) {
        this.errors = error.response.data.errors;
        this.$noty.error("Oops Something went wrong");
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
  }
};
</script>

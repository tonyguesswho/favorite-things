<template>
  <div id="main-bg">
    <div class="home-text">
      <h1>Document Your Favorite Experiences</h1>
      <router-link to="/favorites/create">
        <button type="button" class="btn  btn-lg btn-success mr-5">
          Add Favorite
        </button>
      </router-link>
      <router-link to="/favorites">
        <button type="button" class="btn  btn-lg btn-outline-success ml-5">
          View favorites
        </button>
      </router-link>
    </div>
  </div>
</template>

<style scoped>
#main-bg {
  background-image: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)),
    url(../assets/img/backg.svg);
  height: 100vh;
  background-position: center;
  background-size: cover;
}

.home-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
.home-text h1 {
  color: #fff;
  text-transform: uppercase;
  font-size: 240%;
  font-weight: 300;
  letter-spacing: 1px;
  word-spacing: 4px;
  margin-bottom: 30px;
}
</style>

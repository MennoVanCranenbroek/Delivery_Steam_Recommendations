<template>
<div class="bigdiv">
<div class="games">
    <div class="CardContainer">
      <GameComponent @add-to-my-list="addToMyList" @remove-to-my-list="removeToMyList" class="card" v-for="game in games" v-bind:key="game"
                v-bind:name="game"/>
    </div>
    <div class="mylist">
      <h2>My List</h2>
      <ul>
        <li v-for="game in myList" :key="game">
          {{ game }}
        </li>
      </ul>
    </div>
</div>
<div>
    <button class="predbutton"  @click="predict(name)">predict</button>
    <div class="mylist">
      <h2>predictions</h2>
      <ul>
        <li v-for="game,index in predictions" :key="index">
          {{ game[0] }}
          
        </li>
      </ul>
    </div>
  </div>
</div>
</template>

<script>
import GameComponent from './components/Game.vue';

export default {
  name: 'App',
  components: {
   GameComponent
  },
  data(){
    return{
      games: [],
      myList: [],
      encodedGames: [],
      predictions: []
    }
  },
  mounted() {
    fetch('http://127.0.0.1:5000/GetRandomGames')
      .then(response => response.json())
      .then(data => this.games = data.games)
      

    console.log(this.games)
  },
  methods: {
    addToMyList(game) {
      if (!this.myList.includes(game)) {
        this.myList.push(game);
      }
    },
    removeToMyList(game) {
      const index = this.myList.indexOf(game);
      if (index !== -1) {
        this.myList.splice(index, 1);
      }
    },
    predict(){
      this.encodedGames = this.myList.map(game => encodeURIComponent(game)).join(',');

      console.log(this.encodedGames)
      fetch(`http://127.0.0.1:5000/GetRecommendations?titles=${this.encodedGames}`)
        .then(response => response.json())
        .then(data => this.predictions = data);
    }

  }
}
</script>

<style>
.predbutton{
      height: 20px;
      width: 100%;
      background: darkslateblue;
      border: none;
      border-radius: 15px;
      color: white;
    }
    .predbutton:hover{
      background: lightblue;
    }
.bigdiv{
  gap: 50px;
}
.games{
  display: flex;
  gap: 100px;
}
.mylist{
  color: white
}
body {
  background-color: #1f3050;
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
  
}
</style>

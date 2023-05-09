<template>
    <div class="cardbutton">
      <button class="plus" @click="addToMyList(name)">+</button>
        {{name}}
        <button class="min" @click="removeToMyList(name)">-</button>
    </div>
  </template>
  
  <script>
  
  
  export default {
    name: "GameComponent",
    props: {
      name: String,
    },
    methods: {
    addToMyList(name) {
        this.$emit('add-to-my-list', name);
    },
    removeToMyList(name) {
        this.$emit('remove-to-my-list', name);
    },
    
  }
  }
  </script>
  
  <style scoped>
    .card {
      height: 100%;
      width: 100%;
      overflow: hidden;
    }
      .cardbutton{
        display: flex;
        height: 20px;
        width: 100%;
        background-color: lightblue;
        border: none;
        border-radius: 15px;
        justify-content: space-between;
      }
      .plus{
       
        background-color: lightgreen;
        border: none;
        border-radius: 15px;
        
      }
      .plus:hover{
        background-color: greenyellow;
        border: none;
        border-radius: 15px;
      }
      .min{
        
        background-color: lightcoral;
        border: none;
        border-radius: 15px;
      }
      .min:hover{
        background-color: red;
        border: none;
        border-radius: 15px;
      }
  </style>
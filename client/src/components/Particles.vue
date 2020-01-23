<template lang="pug">
vue-particles.particles-js(color="#dedede"
  :particleOpacity="0.4"
  :particlesNumber="50"
  shapeType="polygon"
  :particleSize="4"
  linesColor="#FFC107"
  :linesWidth="1"
  :lineLinked="true"
  :lineOpacity="0.4"
  :linesDistance="150"
  :moveSpeed="0.3"
  :hoverEffect="true"
  hoverMode="grab"
  :clickEffect="true"
  clickMode="repulse")
</template>

<script>
export default {
  name: 'ParticlesBackground'
}
</script>

<style scoped>
.particles-js {
  z-index: 0;
  position: fixed; /* Sit on top of the page content */
  width: 100%; /* Full width (cover the whole page) */
  height: 100%; /* Full height (cover the whole page) */
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}
</style>

import Vue from 'vue'
import App from './App.vue'
import uk from 'uikit'
import Icons from 'uikit/dist/js/uikit-icons'

uk.use(Icons)

Vue.config.productionTip = false

new Vue({
  render: h => h(App),
}).$mount('#app')

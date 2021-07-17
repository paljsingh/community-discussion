import axios from 'axios'
import store from '../store/store.js'

const axiosInterceptor = axios.create();
axiosInterceptor.defaults.params = {};

axiosInterceptor.interceptors.request.use(function (config) {
  let token = store.state.token
  config.headers['Authorization'] = 'Bearer ' + token
  return config;
}, function (error) {
  // Do something with request error
  return Promise.reject(error);
});

export default axiosInterceptor;
import axios from 'axios'
import store from '../store/index'
const axiosInterceptor = axios.create();

axiosInterceptor.interceptors.request.use(function (config) {
  let token = store.state.account.token
  config.headers['Authorization'] = 'Bearer ' + token
  return config;
}, function (error) {
  // Do something with request error
  return Promise.reject(error);
});

export default axiosInterceptor;
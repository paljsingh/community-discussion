import axios from 'axios'
import {token} from './auth2'

const axiosInterceptor = axios.create();

axiosInterceptor.interceptors.request.use(function (config) {
  config.headers['Authorization'] = 'Bearer ' + token();
  return config;
}, function (error) {
  // Do something with request error
  return Promise.reject(error);
});

export default axiosInterceptor;
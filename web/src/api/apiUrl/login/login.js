import {GET, POST, reUrl} from '../../axiosconfig/axiosconfig'

export default {
    login: function(params) {
        return POST(reUrl + '/token/', params)
    },
    info: function(params) {
        return GET(reUrl + '/user/info/', params)
    }
}

import {DELETE, GET, POST, PUT, reUrl} from '../../axiosconfig/axiosconfig'

export default {
    list: function(params) {
        return GET(reUrl + '/task/task/', params)
    },
    create: function(params) {
        return POST(reUrl + '/task/task/', params)
    },
    retrieve: function(id, params) {
        return GET(reUrl + '/task/task/' + JSON.stringify(id) + '/', params)
    },
    update: function(id, params) {
        return PUT(reUrl + '/task/task/' + JSON.stringify(id) + '/', params)
    },
    execute: function(params) {
        return POST(reUrl + '/task/task/execute/', params)
    },
    operate: function(params) {
        return POST(reUrl + '/task/task/operate/', params)
    },
    delete: function(id) {
        return DELETE(reUrl + '/task/task/' + JSON.stringify(id) + '/')
    }
}

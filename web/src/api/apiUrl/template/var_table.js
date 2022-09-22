import {GET, POST, PUT, DELETE, reUrl} from '../../axiosconfig/axiosconfig'

export default {
    // 作业台
    list: function(params) {
        return GET(reUrl + '/task/var_table/', params)
    },
    create: function(params) {
        return POST(reUrl + '/task/var_table/', params)
    },
    group: function(params) {
        return POST(reUrl + '/task/var_table/group/', params)
    },
    retrieve: function(id, params) {
        return GET(reUrl + '/task/var_table/' + JSON.stringify(id) + '/', params)
    },
    update: function(id, params) {
        return PUT(reUrl + '/task/var_table/' + JSON.stringify(id) + '/', params)
    },
    delete: function(id) {
        return DELETE(reUrl + '/task/var_table/' + JSON.stringify(id) + '/')
    }
}

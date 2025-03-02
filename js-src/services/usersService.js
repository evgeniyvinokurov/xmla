import { AjaxService } from './ajaxService.js';

let UsersService = {
  postEmail: function(email, cb){
    let data = new FormData();
    data.append("email", email);

    AjaxService.doAjaxPost("/user/in/", data, function(data){
			let userId = data.id;
			cb(userId)
		})
	},
}

export { UsersService };

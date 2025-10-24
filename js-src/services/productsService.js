import { ToolsService } from './toolsService.js';
import { AjaxService } from './ajaxService.js';

class ProductsService {
	static picSize = 180
	static categories = []
	static config = {}
	static products = []
	static productsAll = []
	static filters = []
	static preid = 0

	static getByApiAll = function(cb, type = ""){		
		if (ProductsService.preid == 0){
			ProductsService.preid = ToolsService.getRandom(100000, 999999);
		}

		let products = [];
		let self = this;

		let fdata = new FormData();
		fdata.append("type", type);
		fdata.append("preid", ProductsService.preid);

        AjaxService.doAjaxPost("/catalog/out/", fdata, function(data){
			let productsAll = data.products;
			self.config = data.config;
			self.preid = data.preid;
			
			for (var i of productsAll) {
				let product = i;
				product.badge = "";

				if (product){
						product.id = product[self.config.id].trim();
						product.name = product[self.config.name];
						product.description = product[self.config.description];
						product.price = product[self.config.price]*1;
						product.pic = [];

						for (let i=1; i <= product[self.config.pics]*1; i += 1){
							let istr = product.id + (i != 1 ? "."+i :"") + ".png";
    						product.pic.push("/static/pics/" + istr);
						}
				}
				products.push(product);
			}

			let cart = data.cart;
			cb(products, cart)
		})
	}

	static getTotalPrice = function() {
		let sum = 0;
		for(let i of ProductsService.products) {
			sum += i.price;
		}
		return parseFloat(sum).toFixed(2);
	}

	static getCurrentProducts = function() {
       return ProductsService.products = (ProductsService.products.length > 0 ? ProductsService.products : []);
   	}

	static getAllProducts = function(cb, type = "") {
		let self = this;
		ProductsService.getByApiAll(function(data, cart){
			self.productsAll = data;
			cb(data, cart)
		}, type);
	}

	static addProduct = function(id, cb) {	
		if (ProductsService.preid == 0){
			ProductsService.preid = ToolsService.getRandom(100000, 999999);
		}

		let fdata = new FormData();
		fdata.append("id", id);
		fdata.append("preorderid", ProductsService.preid);
		fdata.append("pre", true);
		AjaxService.doAjaxPost("/catalog/preorder/", fdata, function(data){
			cb(data)
		})
	}

	static removeProduct = function(id, cb) {	
		let fdata = new FormData();
		fdata.append("id", id);
		fdata.append("repre", true);
		fdata.append("preorderid", ProductsService.preid);
		AjaxService.doAjaxPost("/catalog/preorder/", fdata, function(data){
			cb(data)
		})
	}

	static makeOrder = function(opts, cb) {
		let idsstr = "";
		let i = 0;
		for (let id of opts.ids) {
			idsstr = idsstr + ((i != 0) ? "-": "") + id;
			i += 1;
		}
		let fdata = new FormData();
		fdata.append("ids", idsstr);
		fdata.append("preorderid", ProductsService.preid);
		fdata.append("userid", opts.userid);
		AjaxService.doAjaxPost("/catalog/order/", fdata, function(data){
			cb(data)
		})
	}

	static cancelOrder = function(opts, cb) {
		let fdata = new FormData();
		
		fdata.append("ids", opts.ids);
		fdata.append("preorderid", ProductsService.preid);
		fdata.append("userid", opts.userid);
		fdata.append("orderid", opts.orderid);
		
		AjaxService.doAjaxPost("/catalog/order/", fdata, function(data){
			cb(data)
		})
	}
};

export { ProductsService };

import { ProductsService } from '../services/productsService.js';
import { UsersService } from '../services/usersService.js';
import { Templater } from '../templater.js';
import { Cart } from './cart.js';

class Catalog {
	bigProduct = function(){
		let thtml = Templater.templates["product-card-big"];
		return Templater.template(thtml, this.main.products[0])
	}

	filtersItems = function(){
		let thtml = Templater.templates["filters-item"];
		let html = "";
		
		for (let f of this.main.filters) {
			html += Templater.template(thtml, f)
		}
		return html;
	}

	removeBadge = function(id){
		document.querySelector(".products-list #id" + id + " .product-card__badge").innerHTML = "";
		let p = document.querySelector(".products-list #id" + id);
		p.classList.remove("added");
		
		let buy = document.querySelector(".products-list #id" + id + " .product-card__buy");
		buy.classList.remove("added");
		buy.innerHTML = "купить";	
	}

	initCatalogEvents = function(){
		let self = this;

		let productscardsbuy = document.querySelectorAll(".product-card .product-card__buy");
		
		for (let el of productscardsbuy){
			el.addEventListener("click", function(e){		
				e.stopPropagation();

				let p = JSON.parse(unescape(this.parentElement.getAttribute("data-src")));

				ProductsService.addProduct(p.id, function(data){
					if (data.status == "ok") {
						if (el.className.indexOf("added") != -1) {
							return false;
						}

						el.innerHTML = "добавлено";
						el.classList.add("added");
						
						self.main.cart.push(p);
						self.main.cartModule.cartReload();	
					}
				})

			});
		}	
		
		let productscards = document.querySelectorAll(".product-card.catalog-card");
		
		for (let el of productscards){
			el.addEventListener("click", function(e){
				let p = JSON.parse(unescape(this.getAttribute("data-src")));
				self.main.showModal(p);
			});
		}	
		
		self.main.cartHeader.addEventListener("click", function(e){
			self.main.cartModule.showhidecart();
		});
		
		self.main.cartTotalEmailOkEl.addEventListener("click", function(e){	
			e.stopPropagation();
			let email = self.main.emailEl.value;
			
			UsersService.postEmail(email, function(userId){
				self.main.userId = userId;
				self.main.email = email;
				
				self.main.showEmail();
			})
		});
		
		self.main.cartTotalBuyEl.addEventListener("click", function(e){	
			e.stopPropagation();
			let ids = [];

			self.main.cartTotalBuyEl.classList.add("hide");
			self.main.cartTotalLoadingEl.classList.remove("hide");

			for (let p of self.main.cart) {
			ids.push(p.id)
			}

			let opts = {}
			opts.ids = ids;
			opts.userid = self.main.userId;

			ProductsService.makeOrder(opts, function(data){     
				self.main.cartTotalLoadingEl.classList.add("hide");

				if (data.orderId) {
				self.main.cartTotalGreetingsOrderEl.innerHTML = "#" + data.orderId;
				self.main.cartTotalGreetingsEl.classList.remove("hide");
				self.main.orderId = data.orderId;
				}

				let crosses = document.querySelectorAll(".cart-main .product .remove-cross");
				for (let c of crosses) {
					c.classList.add("hide");
				}            
			})
		});
		
		self.main.cartTotalGreetingsOrderCancelEl.addEventListener("click", function(e){	
			e.stopPropagation();
			
			let opts = {}
			let ids = []

			for (let p of self.main.cart) {
			ids.push(p.id)
			}

			opts.ids = ids;
			opts.userid = self.main.userId;
			opts.orderid = self.main.orderId;

			ProductsService.cancelOrder(opts, function(data){
			if (data.status == "ok") {          	
				self.main.cartTotalBuyEl.classList.remove("hide");
				self.main.cartTotalGreetingsEl.classList.add("hide"); 
				
				let crosses = document.querySelectorAll(".cart-main .product .remove-cross");
				for (let c of crosses) {
						c.classList.remove("hide");
				}
			}
			}, 3000)
		});
		
		let product = self.main.catalogEl.getAttribute("showThisProduct");
		if (!!product) {		
			for (let p of self.main.products) {
				if (product.indexOf(p.id) != -1) {
					self.main.showModal(p);
					self.main.catalogEl.setAttribute("showThisProduct", null)
				}
			}
		}	
		
		let catalogFiltersEls = document.querySelectorAll(".fblock .filters-item");
		for(let cf of catalogFiltersEls){
			cf.addEventListener("click", function(e){
				e.stopPropagation();
				let type = this.innerHTML == "Все" ? "": this.innerHTML;			
				self.loadCatalog(type);
			});
		} 	
	}

	drawCatalog = function(){
		let productsHtml = this.drawProducts(this.main.products);
		this.main.productsSection.innerHTML = productsHtml;
		
		let bigProductHtml = this.bigProduct();
		this.main.bigProductEl.innerHTML = bigProductHtml;
		
		let filtersHtml = this.filtersItems();
		this.main.fBlockEl.innerHTML = filtersHtml;
	}

	drawProducts = function(products){
		let html = "";

		for (let p of products) { 
			p.added = "";
			let thtml = Templater.templates["product-card"];
			for (let product of this.main.cart){
				if (product.id == p.id) {
					p.badge = "добавлено"
					p.added = "added"
				}
			}		
			html += Templater.template(thtml, p)
		}
		return html;
	}


	loadCatalog = function(type){
		let self = this;

		ProductsService.getAllProducts(function(data, cart){
			if (!!type){     
				history.pushState({}, "", "/catalog/filter/" +type);
			} else {
				history.pushState({}, "", "/catalog/");
			}  
			
			self.main.products = data;            
			self.main.filters = ProductsService.config.filters.split("|");
			self.main.filters.push("Все");
			self.main.cart = cart;
						
			self.drawCatalog();            
			self.initCatalogEvents();

			self.main.cartModule.cartReload();	
		}, type);
	}

	pinModule = function(main){
		this.main = main;
	}
}

export { Catalog };

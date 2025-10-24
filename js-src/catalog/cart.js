import { Templater } from '../templater.js';
import { ToolsService } from '../services/toolsService.js';
import { ProductsService } from '../services/productsService.js';

class Cart {

	showhidecart = function(e){
		let cartEl = document.querySelector(".cart-main");
		
		if (this.main.cart.length > 0){
			this.main.cartshown ? (this.main.cartshown = false, cartEl.classList.add("hide")): (this.main.cartshown = true, cartEl.classList.remove("hide"));
			return false;
		} else {
			this.main.cartshown = false;
			cartEl.classList.add("hide");
			return true;
		}
	}

	cartItemsHtml = function(){
		let html = "";
		
		for (let p of this.main.cart) { 
			let thtml = Templater.templates["product-card-cart"];
			html += Templater.template(thtml, p)
		}
		return html;
	}

	cartItemsImgsHtml = function(){
		let html = "";
		
		for (let p of this.main.cart) { 
			let thtml = Templater.templates["product-card-cart-imgs"];
			html += Templater.template(thtml, p)
		}
		return html;
	}

	calcCart = function(){
		let sum = 0;
		for (let p of this.main.cart){
			sum += p.price*1
		}
		return sum.toFixed(2);
	}

	colorCart = function(){
		this.main.cartTitleEl.style.backgroundColor = this.cartBColor;
		this.main.cartTitleEl.style.color = this.cartColor;
	}

	cartReload = function(){
		let self = this;

		if (self.main.cart.length == 0) {
			self.cartBColor = "transparent";
			self.cartColor = "black";
			self.colorCart();
			
			self.main.cartshown = false;
			
			let cartEl = document.querySelector(".cart-main");
			cartEl.classList.add("hide");
		} else {    
			self.cartBColor = ToolsService.getFromWarmColors();
			self.cartColor = "white"; 
			self.colorCart();
			
			self.main.cartItemsSection.innerHTML = self.cartItemsHtml();	
			self.main.cartItemsImgsSection.innerHTML = self.cartItemsImgsHtml();		
			self.main.cartTotalEl.innerHTML = "Итого: " + self.calcCart(); 
					
			let cartCrosses = document.querySelectorAll(".cart-items .container .remove-cross,.container-imgs .remove-cross");
			for(let c of cartCrosses){
				c.addEventListener("click", function(e){
					e.stopPropagation();
					let p = JSON.parse(unescape(this.parentElement.getAttribute("data-src")));

					ProductsService.removeProduct(p.id, function(data){
						if (data.status == "ok"){
							for (let key in self.main.cart) {
								if (self.main.cart[key].id == p.id) {
									self.main.cart.splice(key, 1);
									self.main.catModule.removeBadge(p.id);
									break;
								}
							}
							
							self.cartReload();
						}
					});
				})
			}
			
			self.main.cartItemsMessageEl.innerHTML = self.main.cart.length;		
		}
	}

	pinModule = function(main){
		this.main = main;
	}
}

export { Cart };

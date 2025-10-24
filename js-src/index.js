import { Templater } from './templater.js';
import { Catalog } from './catalog/catalog.js';
import { Cart } from './catalog/cart.js';

import { ToolsService } from './services/toolsService.js';

class Main {

	cartshown = false;
	cart = [];
	email = "";

	showEmail = function(){
		this.emailHeaderEl.innerHTML = this.email;
		this.emailHeaderEl.classList.remove("hide");
		
		this.cartTotalEmailContainerEl.classList.add("hide");
		this.cartTotalConfirmContainerEl.classList.remove("hide");
	}

	showModal = function(p){
		let self = this;

		self.modalEl.classList.remove("hide");
		
		let thtml = Templater.templates["product-card-modal"];
		let html = Templater.template(thtml, p);
		
		self.modalContentEl.innerHTML = html;
		document.querySelector(".modal .close").addEventListener("click", function(e){		
			self.modalEl.classList.add("hide");
			history.pushState({}, "", window.history.state.prevUrl);
		});	
		
		let itempage = "/catalog/details/" + p.id + ".xml";
				
		if (itempage == location.pathname) {
			history.pushState({prevUrl: "/catalog/" }, "", itempage);
		} else {
			history.pushState({prevUrl: location.pathname }, "", itempage);
		}
	}

	initElements = function(){
		this.productsSection = document.getElementsByClassName("products-list")[0];
		this.cartItemsSection = document.querySelector(".cart-items .container");
		this.cartItemsImgsSection = document.querySelector(".cart-main .container-imgs");
		this.cartTotalEl = document.querySelector(".cart-total__price");
		this.cartTotalEmailOkEl = document.querySelector(".cart-total__email-ok");
		this.cartTotalEmailContainerEl = document.querySelector(".cart-total__email-container");
		this.cartTotalConfirmContainerEl = document.querySelector(".cart-total__confirm-container");
		this.cartTotalLoadingEl = document.querySelector(".cart-total__loading");
		this.cartTotalGreetingsEl = document.querySelector(".cart-total__greetings");
		this.cartTotalGreetingsOrderEl = document.querySelector(".cart-total__greetings-order b");
		this.cartTotalGreetingsOrderCancelEl = document.querySelector(".cart-total__greetings-order .cancel-cross");
		this.cartTotalBuyEl= document.querySelector(".cart-total__confirm");
		this.cartHeader = document.querySelector(".cart");
		this.emailEl = document.querySelector(".cart-total__email");
		this.emailHeaderEl = document.querySelector(".email");
		this.bigProductEl = document.querySelector(".product-card--big");
		this.fBlockEl = document.querySelector(".fblock");
		this.modalContentEl = document.querySelector(".modal-content");
		this.modalEl = document.querySelector(".modal");
		this.catalogEl = document.querySelector(".catalog");
		this.catalogTitleEl = document.querySelector(".title-327");
		this.cartTitleEl = document.querySelector(".cart .cart__title");
		this.cartItemsMessageEl = document.querySelector(".cart-items__message span");	
		
		this.catalogTitleEl.style.backgroundColor = ToolsService.getFromWarmColors();
		this.catalogTitleEl.style.color = "white";
	}

	loadModules = function(){		
		let cat = new Catalog();
		cat.pinModule(this);
		this.catModule = cat;	

		let cart = new Cart();
		cart.pinModule(this);	
		this.cartModule = cart;			

		let type = this.setthisfilters ? this.setthisfilters : "";
    	cat.loadCatalog(type);
	}
}

let init = function(){	
	Templater.makeTemplates(document.getElementsByClassName("template"));

	let main = new Main();

	main.initElements();	
	main.setthisfilters = main.catalogEl.getAttribute("setthisfilters");

	main.loadModules();	 			
}


document.addEventListener("DOMContentLoaded", (event) => {
	init();
});


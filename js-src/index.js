import { Templater } from './templater.js';
import { Catalog } from './catalog/catalog.js';
import { Cart } from './catalog/cart.js';

import { ToolsService } from './services/toolsService.js';

let self = {};

self.cartshown = false;
self.cart = [];
self.email = "";


self.showEmail = function(){
	self.emailHeaderEl.innerHTML = self.email;
	self.emailHeaderEl.classList.remove("hide");
	
	self.cartTotalEmailContainerEl.classList.add("hide");
	self.cartTotalConfirmContainerEl.classList.remove("hide");
}

self.showModal = function(p){
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



self.initElements = function(){
	self.productsSection = document.getElementsByClassName("products-list")[0];
	self.cartItemsSection = document.querySelector(".cart-items .container");
	self.cartItemsImgsSection = document.querySelector(".cart-main .container-imgs");
	self.cartTotalEl = document.querySelector(".cart-total__price");
	self.cartTotalEmailOkEl = document.querySelector(".cart-total__email-ok");
	self.cartTotalEmailContainerEl = document.querySelector(".cart-total__email-container");
	self.cartTotalConfirmContainerEl = document.querySelector(".cart-total__confirm-container");
	self.cartTotalLoadingEl = document.querySelector(".cart-total__loading");
	self.cartTotalGreetingsEl = document.querySelector(".cart-total__greetings");
	self.cartTotalGreetingsOrderEl = document.querySelector(".cart-total__greetings-order b");
	self.cartTotalGreetingsOrderCancelEl = document.querySelector(".cart-total__greetings-order .cancel-cross");
	self.cartTotalBuyEl= document.querySelector(".cart-total__confirm");
	self.cartHeader = document.querySelector(".cart");
	self.emailEl = document.querySelector(".cart-total__email");
	self.emailHeaderEl = document.querySelector(".email");
	self.bigProductEl = document.querySelector(".product-card--big");
	self.fBlockEl = document.querySelector(".fblock");
	self.modalContentEl = document.querySelector(".modal-content");
	self.modalEl = document.querySelector(".modal");
	self.catalogEl = document.querySelector(".catalog");
	self.catalogTitleEl = document.querySelector(".title-327");
	self.cartTitleEl = document.querySelector(".cart .cart__title");
	self.cartItemsMessageEl = document.querySelector(".cart-items__message span");	
	
	self.catalogTitleEl.style.backgroundColor = ToolsService.getFromWarmColors();
    self.catalogTitleEl.style.color = "white";
}

self.loadModules = function(){
	Catalog.pinModule(self);	
	self.Catalog = Catalog;
	
	Cart.pinModule(self);	
}

let init = function(){	
	Templater.makeTemplates(document.getElementsByClassName("template"));
	self.initElements();	

	self.setthisfilters = self.catalogEl.getAttribute("setthisfilters");
	let type = self.setthisfilters ? self.setthisfilters : "";
	
	self.loadModules();	 
    Catalog.loadCatalog(type);				
}

document.addEventListener("DOMContentLoaded", (event) => {
	init();
});

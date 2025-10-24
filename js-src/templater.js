class Templater {
	static templates = {};

	static template = function(html, obj) {	
		let rhtml = html;

		for (let k in obj) {
			let opt = '---' + k + '---';
			rhtml = rhtml.replace(opt, obj[k]);
		}

		rhtml = rhtml.replace("------", escape(JSON.stringify(obj)))
		rhtml = rhtml.replaceAll("ssssss", obj)
		return rhtml;
	}

	static makeTemplates = function(templateselems){
		let result = {};
		
		for (let el of templateselems){
			result[el.id] = el.innerHTML;
		}

		Templater.templates = result;
	}
}
export { Templater };

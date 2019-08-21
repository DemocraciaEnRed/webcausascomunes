/*#manifiesto
#wikis
#galeria
.novedades
.candidates*/

$(function(){
	class Mancha{
		/**
		* @param {string} cssId - Parte del id del elemento contenedor, va a terminar siendo 'mancha-' + cssId
		* @param {string} imgFileName - Nombre de la imagen de la mancha, sin path, con extension
		* @param {float} topPerc - Offset top porcentual (0.0-1.0) desde el top de la section attacheada
		*/
		constructor(cssId, imgFileName, topPerc) {			
			this.cssId = 'mancha-' + cssId;
			this.imgFileName = imgFileName;
			this.topPerc = topPerc;
			//this.section = null;
		}
		
		createHtml(attachToSectionJq){
			//create ele from template
			this.eleJq = Mancha.templateEleJq.clone()
			
			//set id and img
			this.eleJq.attr("id",  this.cssId)
			this.eleJq.find('img').attr("src", Mancha.imgPath + '/' + this.imgFileName);
			
			//set top
			var sectionTop = attachToSectionJq.offset().top
			var sectionHei = attachToSectionJq.outerHeight()
			this.eleJq.css({ top: sectionTop+sectionHei*this.topPerc });	
			
			//add ele to html
			attachToSectionJq.append(this.eleJq)
		}
	}
	Mancha.imgPath = _data_parallax_img_path
	Mancha.templateEleJq = $('.manchas-template')
	
	var sectionManchas = [
		// mirar class Mancha constructor() de arriba para entender valores
		{sectionEleJq: $('#manifiesto'), manchas: [
			new Mancha('mani1', 'group-11.svg', 0.18),
			new Mancha('mani2', 'group-12.svg', 0.22),
			new Mancha('mani3', 'group-13.svg', 0.28),
			new Mancha('mani4', 'group-14.svg', 0.57)]},
		{sectionEleJq: $('#wikis'), manchas: [
			new Mancha('wiki1', 'group-32.svg', 0.60),
			new Mancha('wiki2', 'group-31.svg', 0.22)]}
	]
	
	for (i in sectionManchas){
		section = sectionManchas[i]
		for (j in section.manchas){
			mancha = section.manchas[j]
			mancha.createHtml(section.sectionEleJq)
		}
	}
	this.rellax = new Rellax('.manchas', {
	    wrapper: '#manifiesto',
		relativeToWrapper: true
	  });
})

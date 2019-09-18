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
		* @param {int} speed - Velocidad del parallax (-10-10), negativo se mueve en contra del scroll y positivo a favor
		*/
		constructor(cssId, imgFileName, topPerc, speed) {			
			this.cssId = 'mancha-' + cssId;
			this.imgFileName = imgFileName;
			this.topPerc = topPerc;
			this.speed = speed || 1;
			//this.section = null;
		}
		
		createHtml(attachToEleJq){
			//create ele from template
			this.eleJq = Mancha.templateEleJq.clone()
			
			//set id and img and vel
			this.eleJq.attr("id",  this.cssId)
			this.eleJq.find('img').attr("src", Mancha.imgPath + '/' + this.imgFileName);
			this.eleJq.attr("data-rellax-speed",  this.speed)
			
			//set top
			var sectionTop = attachToEleJq.offset().top
			var sectionHei = attachToEleJq.outerHeight()
			this.eleJq.find('img').css({ top: sectionHei*this.topPerc });	
			
			//add ele to html
			attachToEleJq.append(this.eleJq)
		}
	}
	Mancha.imgPath = _data_parallax_img_path
	Mancha.templateEleJq = $('.manchas-template')
	Mancha.wrapperCssClass = 'manchas-wrapper'
	
	var sectionManchas = [
		// mirar class Mancha constructor() de arriba para entender valores
		{sectionEleJq: $('#manifiesto'), manchas: [
			new Mancha('mani1', 'group-11.svg', 0.18),
			new Mancha('mani2', 'group-12.svg', 0.22,2),
			new Mancha('mani3', 'group-13.svg', 0.28),
			new Mancha('mani4', 'group-14.svg', 0.57, 3)]},
		{sectionEleJq: $('#wikis'), manchas: [
			new Mancha('wiki2', 'group-31.svg', 0.32),
			new Mancha('wiki1', 'group-32.svg', 0.80)]},
		{sectionEleJq: $('.novedades'), manchas: [
			new Mancha('nove1', 'group-41.svg', 0.62),
			new Mancha('nove2', 'group-42.svg', 0.80),
			new Mancha('nove3', 'group-43.svg', 1.30)]}
	]
	
	for (i in sectionManchas){
		section = sectionManchas[i]
		manchasWrapperJq = $('<div/>', {class: Mancha.wrapperCssClass})
		section.sectionEleJq.append(manchasWrapperJq)
		for (j in section.manchas){
			mancha = section.manchas[j]
			mancha.createHtml(manchasWrapperJq)
		}
	}
	this.rellax = new Rellax('.manchas', {
	    wrapper: '#manifiesto',
		relativeToWrapper: true
	  });
})

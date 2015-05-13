/*
 *  cropit - v0.2.0
 *  Customizable crop and zoom.
 *  https://github.com/scottcheng/cropit
 *
 *  Made by Scott Cheng
 *  Based on https://github.com/yufeiliu/simple_image_uploader
 *  Under MIT License
 */
!function(a){var b;b=function(){function a(){}return a.prototype.setup=function(a,b,c,d){var e,f;return null==c&&(c=1),f=b.w/a.w,e=b.h/a.h,this.minZoom="fit"===(null!=d?d.minZoom:void 0)?e>f?f:e:e>f?e:f,this.maxZoom=this.minZoom<1/c?1/c:this.minZoom},a.prototype.getZoom=function(a){return this.minZoom&&this.maxZoom?a*(this.maxZoom-this.minZoom)+this.minZoom:null},a.prototype.getSliderPos=function(a){return this.minZoom&&this.maxZoom?this.minZoom===this.maxZoom?0:(a-this.minZoom)/(this.maxZoom-this.minZoom):null},a.prototype.isZoomable=function(){return this.minZoom&&this.maxZoom?this.minZoom!==this.maxZoom:null},a.prototype.fixZoom=function(a){return a<this.minZoom?this.minZoom:a>this.maxZoom?this.maxZoom:a},a}();var c;c=function(){function c(b,d){var e;this.element=b,this.$el=a(this.element),e={$fileInput:this.$("input.cropit-image-input"),$preview:this.$(".cropit-image-preview"),$zoomSlider:this.$("input.cropit-image-zoom-input"),$previewContainer:this.$(".cropit-image-preview-container")},this.options=a.extend({},c._DEFAULTS,e,d),this.init()}return c._DEFAULTS={exportZoom:1,imageBackground:!1,imageBackgroundBorderWidth:0,imageState:null,allowCrossOrigin:!1,allowDragNDrop:!0,freeMove:!1,minZoom:"fill"},c.PREVIEW_EVENTS=function(){return["mousedown","mouseup","mouseleave","touchstart","touchend","touchcancel","touchleave"].map(function(a){return""+a+".cropit"}).join(" ")}(),c.PREVIEW_MOVE_EVENTS="mousemove.cropit touchmove.cropit",c.ZOOM_INPUT_EVENTS=function(){return["mousemove","touchmove","change"].map(function(a){return""+a+".cropit"}).join(" ")}(),c.prototype.init=function(){var c,d,e,f;return this.image=new Image,this.options.allowCrossOrigin&&(this.image.crossOrigin="Anonymous"),this.$fileInput=this.options.$fileInput.attr({accept:"image/*"}),this.$preview=this.options.$preview.css({backgroundRepeat:"no-repeat"}),this.$zoomSlider=this.options.$zoomSlider.attr({min:0,max:1,step:.01}),this.previewSize={w:this.options.width||this.$preview.width(),h:this.options.height||this.$preview.height()},this.options.width&&this.$preview.width(this.previewSize.w),this.options.height&&this.$preview.height(this.previewSize.h),this.options.imageBackground&&(a.isArray(this.options.imageBackgroundBorderWidth)?this.imageBgBorderWidthArray=this.options.imageBackgroundBorderWidth:(this.imageBgBorderWidthArray=[],[0,1,2,3].forEach(function(a){return function(b){return a.imageBgBorderWidthArray[b]=a.options.imageBackgroundBorderWidth}}(this))),c=this.options.$previewContainer,this.$imageBg=a("<img />").addClass("cropit-image-background").attr("alt","").css("position","absolute"),this.$imageBgContainer=a("<div />").addClass("cropit-image-background-container").css({position:"absolute",zIndex:0,left:-this.imageBgBorderWidthArray[3]+window.parseInt(this.$preview.css("border-left-width")),top:-this.imageBgBorderWidthArray[0]+window.parseInt(this.$preview.css("border-top-width")),width:this.previewSize.w+this.imageBgBorderWidthArray[1]+this.imageBgBorderWidthArray[3],height:this.previewSize.h+this.imageBgBorderWidthArray[0]+this.imageBgBorderWidthArray[2]}).append(this.$imageBg),this.imageBgBorderWidthArray[0]>0&&this.$imageBgContainer.css({overflow:"hidden"}),c.css("position","relative").prepend(this.$imageBgContainer),this.$preview.css("position","relative"),this.$preview.hover(function(a){return function(){return a.$imageBg.addClass("cropit-preview-hovered")}}(this),function(a){return function(){return a.$imageBg.removeClass("cropit-preview-hovered")}}(this))),this.initialOffset={x:0,y:0},this.initialZoom=0,this.initialZoomSliderPos=0,this.imageLoaded=!1,this.moveContinue=!1,this.zoomer=new b,this.options.allowDragNDrop&&jQuery.event.props.push("dataTransfer"),this.bindListeners(),this.$zoomSlider.val(this.initialZoomSliderPos),this.setOffset((null!=(d=this.options.imageState)?d.offset:void 0)||this.initialOffset),this.zoom=(null!=(e=this.options.imageState)?e.zoom:void 0)||this.initialZoom,this.loadImage((null!=(f=this.options.imageState)?f.src:void 0)||null)},c.prototype.bindListeners=function(){return this.$fileInput.on("change.cropit",this.onFileChange.bind(this)),this.$preview.on(c.PREVIEW_EVENTS,this.onPreviewEvent.bind(this)),this.$zoomSlider.on(c.ZOOM_INPUT_EVENTS,this.onZoomSliderChange.bind(this)),this.options.allowDragNDrop?(this.$preview.on("dragover.cropit dragleave.cropit",this.onDragOver.bind(this)),this.$preview.on("drop.cropit",this.onDrop.bind(this))):void 0},c.prototype.unbindListeners=function(){return this.$fileInput.off("change.cropit"),this.$preview.off(c.PREVIEW_EVENTS),this.$preview.off("dragover.cropit dragleave.cropit drop.cropit"),this.$zoomSlider.off(c.ZOOM_INPUT_EVENTS)},c.prototype.reset=function(){return this.zoom=this.initialZoom,this.offset=this.initialOffset},c.prototype.onFileChange=function(){var a;return"function"==typeof(a=this.options).onFileChange&&a.onFileChange(),this.loadFileReader(this.$fileInput.get(0).files[0])},c.prototype.loadFileReader=function(a){var b;return b=new FileReader,(null!=a?a.type.match("image"):void 0)?(this.setImageLoadingClass(),b.readAsDataURL(a),b.onload=this.onFileReaderLoaded.bind(this),b.onerror=this.onFileReaderError.bind(this)):null!=a?this.onFileReaderError():void 0},c.prototype.onFileReaderLoaded=function(a){return this.reset(),this.loadImage(a.target.result)},c.prototype.onFileReaderError=function(){var a;return"function"==typeof(a=this.options).onFileReaderError?a.onFileReaderError():void 0},c.prototype.onDragOver=function(a){return a.preventDefault(),a.dataTransfer.dropEffect="copy",this.$preview.toggleClass("cropit-drag-hovered","dragover"===a.type)},c.prototype.onDrop=function(a){var b;return a.preventDefault(),a.stopPropagation(),b=Array.prototype.slice.call(a.dataTransfer.files,0),b.some(function(a){return function(b){return b.type.match("image")?(a.loadFileReader(b),!0):void 0}}(this)),this.$preview.removeClass("cropit-drag-hovered")},c.prototype.loadImage=function(a){var b;return this.imageSrc=a,this.imageSrc?("function"==typeof(b=this.options).onImageLoading&&b.onImageLoading(),this.setImageLoadingClass(),this.image.onload=this.onImageLoaded.bind(this),this.image.onerror=this.onImageError.bind(this),this.image.src=this.imageSrc):void 0},c.prototype.onImageLoaded=function(){var a;return this.setImageLoadedClass(),this.setOffset(this.offset),this.$preview.css("background-image","url("+this.imageSrc+")"),this.options.imageBackground&&this.$imageBg.attr("src",this.imageSrc),this.imageSize={w:this.image.width,h:this.image.height},this.setupZoomer(),this.imageLoaded=!0,"function"==typeof(a=this.options).onImageLoaded?a.onImageLoaded():void 0},c.prototype.onImageError=function(){var a;return"function"==typeof(a=this.options).onImageError?a.onImageError():void 0},c.prototype.setImageLoadingClass=function(){return this.$preview.removeClass("cropit-image-loaded").addClass("cropit-image-loading")},c.prototype.setImageLoadedClass=function(){return this.$preview.removeClass("cropit-image-loading").addClass("cropit-image-loaded")},c.prototype.getEventPosition=function(a){var b,c,d,e;return(null!=(b=a.originalEvent)&&null!=(c=b.touches)?c[0]:void 0)&&(a=null!=(d=a.originalEvent)&&null!=(e=d.touches)?e[0]:void 0),a.clientX&&a.clientY?{x:a.clientX,y:a.clientY}:void 0},c.prototype.onPreviewEvent=function(b){return this.imageLoaded?(this.moveContinue=!1,this.$preview.off(c.PREVIEW_MOVE_EVENTS),"mousedown"===b.type||"touchstart"===b.type?(this.origin=this.getEventPosition(b),this.moveContinue=!0,this.$preview.on(c.PREVIEW_MOVE_EVENTS,this.onMove.bind(this))):a(document.body).focus(),b.stopPropagation(),!1):void 0},c.prototype.onMove=function(a){var b;return b=this.getEventPosition(a),this.moveContinue&&b&&this.setOffset({x:this.offset.x+b.x-this.origin.x,y:this.offset.y+b.y-this.origin.y}),this.origin=b,a.stopPropagation(),!1},c.prototype.setOffset=function(a){return this.offset=this.fixOffset(a),this.$preview.css("background-position",""+this.offset.x+"px "+this.offset.y+"px"),this.options.imageBackground?this.$imageBg.css({left:this.offset.x+this.imageBgBorderWidthArray[3],top:this.offset.y+this.imageBgBorderWidthArray[0]}):void 0},c.prototype.fixOffset=function(a){var b;return this.imageLoaded?(b={x:a.x,y:a.y},this.options.freeMove||(b.x=this.imageSize.w*this.zoom>=this.previewSize.w?Math.min(0,Math.max(b.x,this.previewSize.w-this.imageSize.w*this.zoom)):Math.max(0,Math.min(b.x,this.previewSize.w-this.imageSize.w*this.zoom)),b.y=this.imageSize.h*this.zoom>=this.previewSize.h?Math.min(0,Math.max(b.y,this.previewSize.h-this.imageSize.h*this.zoom)):Math.max(0,Math.min(b.y,this.previewSize.h-this.imageSize.h*this.zoom))),b.x=this.round(b.x),b.y=this.round(b.y),b):a},c.prototype.onZoomSliderChange=function(){var a;if(this.imageLoaded)return this.zoomSliderPos=Number(this.$zoomSlider.val()),a=this.zoomer.getZoom(this.zoomSliderPos),this.setZoom(a)},c.prototype.enableZoomSlider=function(){var a;return this.$zoomSlider.removeAttr("disabled"),"function"==typeof(a=this.options).onZoomEnabled?a.onZoomEnabled():void 0},c.prototype.disableZoomSlider=function(){var a;return this.$zoomSlider.attr("disabled",!0),"function"==typeof(a=this.options).onZoomDisabled?a.onZoomDisabled():void 0},c.prototype.setupZoomer=function(){return this.zoomer.setup(this.imageSize,this.previewSize,this.options.exportZoom,this.options),this.zoom=this.fixZoom(this.zoom),this.setZoom(this.zoom),this.isZoomable()?this.enableZoomSlider():this.disableZoomSlider()},c.prototype.setZoom=function(a){var b,c,d,e,f;return a=this.fixZoom(a),f=this.round(this.imageSize.w*a),e=this.round(this.imageSize.h*a),d=this.zoom,b=this.previewSize.w/2-(this.previewSize.w/2-this.offset.x)*a/d,c=this.previewSize.h/2-(this.previewSize.h/2-this.offset.y)*a/d,this.zoom=a,this.setOffset({x:b,y:c}),this.zoomSliderPos=this.zoomer.getSliderPos(this.zoom),this.$zoomSlider.val(this.zoomSliderPos),this.$preview.css("background-size",""+f+"px "+e+"px"),this.options.imageBackground?this.$imageBg.css({width:f,height:e}):void 0},c.prototype.fixZoom=function(a){return this.zoomer.fixZoom(a)},c.prototype.isZoomable=function(){return this.zoomer.isZoomable()},c.prototype.getCroppedImageData=function(b){var c,d,e,f,g;return this.imageSrc?(f={type:"image/png",quality:.75,originalSize:!1,fillBg:"#fff"},b=a.extend({},f,b),e={w:this.previewSize.w,h:this.previewSize.h},g=b.originalSize?1/this.zoom:this.options.exportZoom,c=a("<canvas />").attr({width:e.w*g,height:e.h*g}).get(0),d=c.getContext("2d"),"image/jpeg"===b.type&&(d.fillStyle=b.fillBg,d.fillRect(0,0,c.width,c.height)),d.drawImage(this.image,this.offset.x*g,this.offset.y*g,this.zoom*g*this.imageSize.w,this.zoom*g*this.imageSize.h),c.toDataURL(b.type,b.quality)):null},c.prototype.getImageState=function(){return{src:this.imageSrc,offset:this.offset,zoom:this.zoom}},c.prototype.getImageSrc=function(){return this.imageSrc},c.prototype.getOffset=function(){return this.offset},c.prototype.getZoom=function(){return this.zoom},c.prototype.getImageSize=function(){return this.imageSize?{width:this.imageSize.w,height:this.imageSize.h}:null},c.prototype.getPreviewSize=function(){return{width:this.previewSize.w,height:this.previewSize.h}},c.prototype.setPreviewSize=function(a){return(null!=a?a.width:void 0)>0&&(null!=a?a.height:void 0)>0?(this.previewSize={w:a.width,h:a.height},this.$preview.css({width:this.previewSize.w,height:this.previewSize.h}),this.options.imageBackground&&this.$imageBgContainer.css({width:this.previewSize.w+this.imageBgBorderWidthArray[1]+this.imageBgBorderWidthArray[3],height:this.previewSize.h+this.imageBgBorderWidthArray[0]+this.imageBgBorderWidthArray[2]}),this.imageLoaded?this.setupZoomer():void 0):void 0},c.prototype.disable=function(){return this.unbindListeners(),this.disableZoomSlider(),this.$el.addClass("cropit-disabled")},c.prototype.reenable=function(){return this.bindListeners(),this.enableZoomSlider(),this.$el.removeClass("cropit-disabled")},c.prototype.round=function(a){return+(Math.round(100*a)+"e-2")},c.prototype.$=function(a){return this.$el?this.$el.find(a):null},c}();var d,e;d="cropit",e={init:function(b){return this.each(function(){var e;return a.data(this,d)?void 0:(e=new c(this,b),a.data(this,d,e))})},destroy:function(){return this.each(function(){return a.removeData(this,d)})},isZoomable:function(){var a;return a=this.first().data(d),null!=a?a.isZoomable():void 0},"export":function(a){var b;return b=this.first().data(d),null!=b?b.getCroppedImageData(a):void 0},imageState:function(){var a;return a=this.first().data(d),null!=a?a.getImageState():void 0},imageSrc:function(b){var c;return null!=b?this.each(function(){var c;return c=a.data(this,d),null!=c&&c.reset(),null!=c?c.loadImage(b):void 0}):(c=this.first().data(d),null!=c?c.getImageSrc():void 0)},offset:function(b){var c;return null!=b&&null!=b.x&&null!=b.y?this.each(function(){var c;return c=a.data(this,d),null!=c?c.setOffset(b):void 0}):(c=this.first().data(d),null!=c?c.getOffset():void 0)},zoom:function(b){var c;return null!=b?this.each(function(){var c;return c=a.data(this,d),null!=c?c.setZoom(b):void 0}):(c=this.first().data(d),null!=c?c.getZoom():void 0)},imageSize:function(){var a;return a=this.first().data(d),null!=a?a.getImageSize():void 0},previewSize:function(b){var c;return null!=b?this.each(function(){var c;return c=a.data(this,d),null!=c?c.setPreviewSize(b):void 0}):(c=this.first().data(d),null!=c?c.getPreviewSize():void 0)},disable:function(){return this.each(function(){var b;return b=a.data(this,d),b.disable()})},reenable:function(){return this.each(function(){var b;return b=a.data(this,d),b.reenable()})}},a.fn.cropit=function(a){return e[a]?e[a].apply(this,[].slice.call(arguments,1)):e.init.apply(this,arguments)}}(window.jQuery);
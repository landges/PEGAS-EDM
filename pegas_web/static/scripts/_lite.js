PDA.utils={entityify:function(t){var n={"<":"&lt;",">":"&gt;","&":"&amp;",'"':"&quot;"};return t.replace(/[<>&"]/g,function(t){return n[t]})},queryToObject:function(t){var n={};if(t&&"string"==typeof t)return t.split("&").forEach(function(t,e){var a=t.split("=");n[a[0]]=a[1]}),n},html2text:function(t){return t?t.replace(/<\s*(\/?)([^\/>\s]+)\s*[^>]*>/g,function(t,n,e){var a="/"===n;switch(e){case"h1":case"h2":case"h3":case"h4":case"h5":case"h6":case"pre":case"p":case"br":case"ol":case"ul":case"dl":return"\n";case"div":case"address":case"fieldset":case"form":case"blockquote":case"dt":case"dd":case"tr":return a?"\n":"";case"hr":return"\n----------------------------------------\n";case"li":return a?"\n":"* ";case"table":return a?"":"\n";case"td":case"th":return a?" ":""}return""}).replace(/^[\u0020\u00a0]+$/gm,"").replace(/^\n|\n$/,""):""},counter:function(t,n){var e=new Image;return n||(n="https://yastatic.net/lego/_/La6qi18Z8LwgnZdsAr1qy1GwCwo.gif"),e.src=location.protocol+"//clck.yandex.ru/click/"+t+"/*"+n},bindTouchStart:function(t,n){function e(t){if(1===t.which)return n.apply(this,arguments)}t.bind("mousedown",e).one("touchstart",function(){$(this).unbind("mousedown",e)}).bind("touchstart",n)}},Array.prototype.forEach||(Array.prototype.forEach=function(t){"use strict";if(void 0===this||null===this)throw new TypeError;var n=Object(this),e=n.length>>>0;if("function"!=typeof t)throw new TypeError;for(var a=arguments[1],c=0;c<e;c++)c in n&&t.call(a,n[c],c,n)}),PDA.Actions=function(){var t=[],n=function(n,e,a){t.forEach(function(t,c){t.name==e&&t.callback(n,a)})};return $(".pda-action").click(function(t){var e=$(t.target),a=e.attr("data-action"),c=e.attr("data-params");"A"==e[0].nodeName&&t.preventDefault(),n(t,a,c)}),{add:function(n,e){t.push({name:n,callback:e})},run:n}}(),function(t){var n="yaCounter16082899";function e(t,n){n.params(function(t){for(var n,e,a,c=t.split(":"),r=c.pop();c.length;)n=r,e=c.pop(),a=void 0,(a={})[e]=n,r=a;return r}($(t).attr("data-counter")))}function a(){var a=t[n];return!!a&&($(".pda-counter-show").each(function(){e(this,a)}),$(document).delegate(".pda-counter","click",function(){var n=$(this).attr("href");if(e(this,a),n)return t.setTimeout(function(){t.location=n},100),!1}),!0)}$(function(){!a()&&t.yandex_metrika_callbacks&&t.yandex_metrika_callbacks.push(a)})}(window),PDA.Actions.add("blockquote-toggle",function(t){$(t.target).parent().toggleClass("b-quote_minimized")}),PDA.Actions.add("messages-actions",function(t){var n=$("form").eq(0);n.append('<input type="hidden" name="more" value="1"/>'),n.submit()}),PDA.Actions.add("messages-mark",function(t){PDA.messages.sendAction("mark")}),PDA.Actions.add("messages-unmark",function(t){PDA.messages.sendAction("unmark")}),PDA.Actions.add("messages-tospam",function(t){PDA.messages.sendAction("tospam")}),PDA.Actions.add("messages-notspam",function(t){PDA.messages.sendAction("notspam")}),PDA.Actions.add("check-all",function(t){PDA.messages.checkAll(t)}),$(document).keypress(function(t){if(13==t.which&&"request"==t.target.name)return $("input[name=search]").click(),!1});
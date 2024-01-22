console.debug("loaded util.js")


    var data_idx = 0;
    var keys_visible_default = " img img_lnk price ";

            function addData( responseText ) { // id img_lnk descr price hash
                console.debug( responseText );

                key_idx = 0 ; img_src_idx=1; img_lnk_idx=2; descr_idx=3; price_idx=4;
                var data = JSON.parse( responseText);
                var val = data;

                itm_div = '';
                data.priceVB = data.price.includes("VB") ? "VB":"";
                data.price = data.price.replace(" VB","");
                k="href";
                itm_div += '<a class="d_' + k + '" href="' + data[k] + '">';
                for ( var k in data ) {
                    if ( null == data[k] ) {
                    } else if ( "img" == k ) {
                        itm_div += '<img class="d_' + k + '" src="' + data[k] + '"/>';
                    } else if ( data[k].startsWith("http") ) {
                        // itm_div += '<a class="d_' + k + '" href="' + data[k] + '"></a>';
                    } else  {
                        itm_div += '<div class="d_' + k + '">' + data[k] + '</div>';
                    }
                    // console.debug( k + " -> " + data[k] );
                }
                itm_div += '</a>';
                /*
                itm_div = '';
                itm_div += '<a   class="d_href" href="' + val[img_lnk_idx] + '">"';
                itm_div += '<img class="d_img" src="' + val[img_src_idx] + '"/>';
                itm_div += '<div class="d_price">' + val[price_idx].replace(" VB","") + '</div>';
                itm_div += '<div class="d_priceVB">' + (val[price_idx].includes("VB") ? "VB":"") + '</div>';
                itm_div += '<div class="d_idx">' + val[key_idx] + '</div>';
                itm_div += '</a>';
                */
                //
                var newElement = document.createElement('div');
                newElement.classList.add("d_offer");
                newElement.classList.add("sortableDiv");
                newElement.innerHTML = itm_div;
                newElement.id = data['key'];
                document.getElementById("datas").appendChild(newElement);

                // add toggler
                for ( var k in data ) {
                    key = "ctrl_"+k;
                    if ( null == document.getElementById( key )) {
                        newElement = document.createElement('div');
                        newElement.id = key;
                        newElement.classList.add("ctrlDiv");
                        newElement.classList.add("button");
                        newElement.setAttribute("srcId","d_" + k );
                        newElement.setAttribute("onclick","ctrl_clk( event, this, 'd_" + k + "');");
                        // newElement.setAttribute("onclick","changeClassCss( '.d_" + k + "', 'display', 'none', 'block');");
                        newElement.innerHTML = k;
                        document.getElementById("ctrl").appendChild(newElement);
                        // preset ...
                        if ( !keys_visible_default.includes( " " + k + " " ) ) {
                            ctrl_clk( null, newElement, "d_" + k );
                        }
                    }
                }

            }

            /*
                click -> sort
                click+shift -> add to sort
                click+ctrl -> toggle display
            */
            function ctrl_clk( event, elem, k ) {
                if ( null == event ) {
                    changeClassCss( "." + k, 'display', 'none', 'block');
                    elem.classList.toggle("ctrlDivDisabled");
                } else if ( event.shiftKey && event.ctrlKey ) {
                    var k_ = k.startsWith("d_") ? k.substring(2) : k;
                    changeClassCss( "." + k, 'display', 'none', 'none'); // enforce hidden
                    elem.classList.toggle("ctrlDivGrouped");
                    document.getElementById("sortKeys").value = document.getElementById("sortKeys").value + " " + k_ + ":G";
                    sortDivElements();
                } else if ( event.ctrlKey ) {
                    changeClassCss( "." + k, 'display', 'none', 'block');
                    elem.classList.toggle("ctrlDivDisabled");
                } else if ( event.shiftKey ) {
                    var k_ = k.startsWith("d_") ? k.substring(2) : k;
                    document.getElementById("sortKeys").value = document.getElementById("sortKeys").value + " " + k_;
                    sortDivElements();
                } else {
                    var k_ = k.startsWith("d_") ? k.substring(2) : k;
                    document.getElementById("sortKeys").value = k_;
                    sortDivElements();
                }
            }

            function pollData() {
                if (document.getElementById('liveUpdate').checked) {
                    var d = new Date();
                    var datestring = ("0" + d.getDate()).slice(-2) + "-" + ("0"+(d.getMonth()+1)).slice(-2) + "-" +
                            d.getFullYear() + " " + ("0" + d.getHours()).slice(-2) + ":" + ("0" + d.getMinutes()).slice(-2) +
                            ":" + ("0" + d.getSeconds()).slice(-2);
                    document.getElementById('liveUpdateLabel').innerHTML="liveUpdate " + datestring;
                    var xhr = new XMLHttpRequest();
                    xhr.onreadystatechange = function() {
                        if (xhr.readyState === 4 && xhr.status === 200) {
                            addData( xhr.responseText);
                            data_idx=data_idx+1;
                            setTimeout(pollData, 10);
                        }
                    };
                    xhr.open("GET", "/json?idx=" + data_idx , true);
                    xhr.send();
                } // if liveUpdate
            }
            setInterval(pollData, 5000);






      function sortDivElements() {
        var container = document.getElementById("datas");
        var divList = Array.prototype.slice.call(container.getElementsByClassName("sortableDiv"));
        var sortKeys = (document.getElementById("sortKeys").value + " price:n").split(" ");
        var groupKeys = [];
        for(let i = 0; i < sortKeys.length; i++) {
            if (sortKeys[i].length > 3 ){
                if(!sortKeys[i].startsWith("d_")) {
                    sortKeys[i] = "d_" +sortKeys[i];
                }
                if(sortKeys[i].endsWith(":G")) {
                    sortKeys[i] = sortKeys[i].replace(":G","");
                    groupKeys.push(sortKeys[i]);
                }
            }
        }


        divList.sort(function (a, b) {
            for (let key of sortKeys) {
              if ("" != key) {
                var keyNum = key.includes(":n") || "d_price".includes( key );
                if (keyNum) {
                    key = key.replace(":n","");
                }
                key = key.replace(":G",""); // remove Grouping hint -->  Sort-it, show only Once and hide following ...
                var a_ = a.getElementsByClassName(key);
                var aKey = undefined == a_ || a_.length < 1 ? "" : a_[0].innerText;
                var b_ = b.getElementsByClassName(key);
                var bKey = undefined == b_ || b_.length < 1 ? "" : b_[0].innerText;
                if (aKey == bKey) {
                } else if (keyNum) {
                    aKey = aKey.replace(".","");
                    bKey = bKey.replace(".","");
                    return 1*aKey < 1*bKey ? -1 : 1 ;
                } else {
                    return aKey.localeCompare(bKey);
                } // diff
              } // key
            } // keys
            return 0; // If all keys are equal
        });

        // [ div , div , div ]
        // div-Group1 ( val1 ) >    [   div-Group2 ( val2.1 ) >  [ div , div ] ,  div-Group2 ( val2.2 ) >  div   ]
        var divGroupedList = [ document.createElement('div') ]; // Base 1 !!!! - root == [0]
        for (var i = 0; i < divList.length; i++) {
            // handle grouping - show group-header, hide repeats ...
            // check if matches current group - already sorted !!!
            //   -> if it is not matching
            for (var groupKey_i = 1; groupKey_i <= groupKeys.length; groupKey_i++) { // Base 1 !!!! - root == [0]
                val_div = divList[ i ].getElementsByClassName( groupKeys[ groupKey_i - 1 /* Base1->Base0 */] )[0] ;
                val = null == val_div ? "" : val_div.innerText;
                group_div = divGroupedList[ groupKey_i ];
                // 1. new / 2. matches val / 3. changed val
                if ( null == group_div || null == group_div.firstChild || val.trim() != group_div.firstChild.innerText.trim() /*for some reason sometimes spaces skipped*/ ) { // changed or new
                    group_div = document.createElement('div'); // neue group
                    group_div.classList.add("d_group");
                    group_div.innerHTML = val_div.outerHTML ; // clone value for group ...
                    group_div.firstChild.classList.add("d_group_val");
                    divGroupedList[ groupKey_i - 1 ].appendChild( group_div ); // build tree up to root ...
                    divGroupedList[ groupKey_i ] = group_div; // build short ref to current branch
                    divGroupedList[ groupKey_i + 1 ] = null; // invalidate - force diff in next level
                    //
                }
            } // build grouping-path
            group_div.appendChild( divList[ i ] );
        } // group all divs ...

        if (divGroupedList.length > 0) {
            divList = [ divGroupedList[0] ];
        }
        // show
        container.innerHTML = "";
        for (var i = 0; i < divList.length; i++) {
            container.appendChild(divList[i]);
        }

        // --------------------------------------------------------------


      }

        //  changeClassCss( ".element", "display", "none");
        function changeClassCss( cssSelector, prop, val, val2 ) {
            const stylesheet = document.styleSheets[0];
            let elementRules = null;
            for(let i = 0; i < stylesheet.cssRules.length; i++) {
              if(stylesheet.cssRules[i].selectorText === cssSelector) {
                elementRules = stylesheet.cssRules[i];
                if (null != val2) {
                   val = val == elementRules.style.getPropertyValue(prop) ? val2 : val;
                }
                elementRules.style.setProperty(prop, val);

              }
            }
            if (null == elementRules){
                stylesheet.insertRule( cssSelector + " {" + prop + ": " + val + "}", 1);
                stylesheet.addRule( cssSelector ,  prop + ": " + val , 1);
            }

        }
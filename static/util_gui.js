    console.debug("loaded util_gui.js")

    function sortDivElements() {
        var container = document.getElementById("datas");
        var divList = Array.prototype.slice.call(container.getElementsByClassName("sortableDiv"));
        var sortKeys = (document.getElementById("sortKeys").value + " price:n").split(" ");
        var groupKeys = [];
        /*
            img -> sort by img_hash
            img:G -> sort by img_hash / group by img_hash but show "img"

        */
        for(let i = 0; i < sortKeys.length; i++) {
            if (sortKeys[i].length > 1 ){
                skey_parts = sortKeys[i].split(/:/);
                skey = skey_parts[0];
                skey_param = skey_parts.length > 1 ? skey_parts[1] :  "";
                // use "_hash" for not normal sortable types like image ...
                if ("img:G" == sortKeys[i]) {
                    changeClassCss( ".d_" + skey, 'display', 'none', 'none');
                }
                if ("img_hash ".includes( skey + "_hash" )){
                    skey = skey + "_hash";
                    console.debug( "util_gui::sortDivElements  substitute key " + sortKeys[i] + " => " + skey + "  (use '_hash' for not normal sortable types like image ...)");
                }
                //
                if(!skey.startsWith("d_")) {
                    skey = "d_" + skey;
                }
                sortKeys[i] = skey;
                if("G" == skey_param) {
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
        if (groupKeys.length>0) {
            var group_div = null;
            var divGroupedList = [ document.createElement('div') ]; // Base 1 !!!! - root == [0]
            for (var i = 0; i < divList.length; i++) {
                // handle grouping - show group-header, hide repeats ...
                // check if matches current group - already sorted !!!
                //   -> if it is not matching
                for (var groupKey_i = 1; groupKey_i <= groupKeys.length; groupKey_i++) { // Base 1 !!!! - root == [0]
                    var groupKey = groupKeys[ groupKey_i - 1 ];/* Base1->Base0 */
                    val_div = divList[ i ].getElementsByClassName( groupKey )[0] ;
                    val = undefined === val_div || null == val_div ? "" : val_div.innerText;
                    val_div = divGroupedList[ groupKey_i ];
                    group_div_val = null == group_div || null == group_div.firstChild ? "" : group_div.key ? group_div.key : group_div.firstChild.innerText;
                    // 1. new / 2. matches val / 3. changed val
                    // if ( null == group_div || null == group_div.firstChild || val.trim() != group_div.firstChild.innerText.trim() /*for some reason sometimes spaces skipped*/ ) { // changed or new
                    if ( null == group_div || val.trim() != group_div_val.trim() /*for some reason sometimes spaces skipped*/ ) { // changed or new
                        group_div = document.createElement('div'); // neue group
                        group_div.classList.add("d_group");
                        if ( groupKey.endsWith("_hash") ){ // replace ... img_hash by img
                            val_div = divList[ i ].getElementsByClassName( groupKey.replace(/_hash$/,"") )[0];
                            group_div.key = val; // es content is different - store key for comparison
                        }
                        group_div.innerHTML = val_div ? val_div.outerHTML : "<div class='" + groupKey + "'>undefined</div>" ; // clone value for group ... OR create group if no key existed
                        group_div.firstChild.classList.add("d_group_val");
                        divGroupedList[ groupKey_i - 1 ].appendChild( group_div ); // build tree up to root ...
                        divGroupedList[ groupKey_i ] = group_div; // build short ref to current branch
                        divGroupedList[ groupKey_i + 1 ] = null; // invalidate - force diff in next level
                        //
                    }
                } // build grouping-path
                group_div.appendChild( divList[ i ] );
            } // group all divs ...
            divList = [ divGroupedList[0] ];
        }

        // show
        container.innerHTML = "";
        for (var i = 0; i < divList.length; i++) {
            container.appendChild(divList[i]);
        }

        // --------------------------------------------------------------



    }

function processBatch(id, pw){
    var reporter = $('#batchstatus'+id);
    var textarea = $('#batch'+id+'_ignoreme_');
    var addbtn = $('#addbatch'+id);

    var reading = textarea.val();

    var extracted = [];
    var len;
    var counter;
    var invalid = [];

    var preprocess = function(reading){
        var processed = [];

        var possible = reading.trim().split('\n');
        var errors = [];
        var basemsg;

        for(var i=0;i<possible.length;i++){
            var cleaned = parseInt(possible[i].trim());

            if(!isNaN(cleaned)) {
                processed.push(cleaned);
            } else {
                errors.push(possible[i]);
            }
        }

        if(processed.length === 0){
            return [undefined, errors]
        }
        return [processed, errors];
    };
    var errors_render = function(){
        var errstring="";

        for(var i=0;i<invalid.length;i++){
            console.log(invalid[i]);
            if(typeof invalid[i] == 'string' || invalid[i] instanceof String){
                invalid[i] = invalid[i].replace(/("|')/g, "");
            }
            errstring+=invalid[i]+"<br />";
        }

        return '<div style="overflow: auto; height: 180px;"><div>'+errstring+"</div></div>";
    };
    var finalcase = function(){
        for(var i=0;i<extracted.length;i++){
            pw.addPublication(extracted[i]);
        }

        if(invalid.length == 0){
            reporter.text(" Finished processing "+len+"/"+len+".");

        } else {
            var result = " Finished processing "+len+"/"+len+'. With <a style="color: #08c;" id="errors_'+id+'" href="javascript:void(0);">'+invalid.length+'</a> invalid publications numbers.';

            console.log(result);
            reporter.html(result);
        }

        textarea.removeProp('disabled');
        addbtn.removeProp('disabled');

        $('#errors_'+id).popover({
            'container': '#modal-batch',
            'html': 'true',
            'placement': 'top',
            'content': errors_render(),
            'trigger': 'click',
            'title': 'Unparsable PubMed Identifications'
        });
    };
    var getpubmed = function(pubmedid){

        var result = "";
        $.ajax({
            type: "GET",
            url: "api/pubmed?pmid="+pubmedid,
            data: { pmid: pubmedid},
            success: function (data) {
                data['id'] = ''+pubmedid;

                extracted.push(data);
                console.log(data);
                counter++;
                reporter.text(basemsg+" Processing "+counter+"/"+len+ ", please wait.");

                // limit case, ended processing all requests
                if(counter == len){
                    finalcase();
                }
            },
            error: function() {
                counter++;
                reporter.text(basemsg+" Processing "+counter+"/"+len+ ", please wait.");
                invalid.push(pubmedid);

                // limit case, ended processing all requests
                if(counter == len){
                    finalcase();
                }
              }
          });
    };

    reporter.text('Finding PubMed References.');

    textarea.prop('disabled', 'true');
    addbtn.prop('disabled', 'true');

    var processed = preprocess(reading);

    if(processed[0] == undefined){
        reporter.text('No references found at all.')
        bootbox.alert('Invalid list of PubMed identifications.<br />The list must be composed of a series of PubMed identifications numbers separated by break lines.<br /><br /> For Example:<br />22875554<br />20981467<br />20981468');

        textarea.removeProp('disabled');
        addbtn.removeProp('disabled');

    } else {
        len = processed[0].length;
        counter = 0;
        basemsg = 'Found '+len+' references. ';

        if(processed[1].length != 0){
            $.merge(invalid, processed[1]);
        }
        reporter.text(basemsg);

        for(var i=0;i<len;i++){
            var identification = processed[0][i];
            getpubmed(identification);

        }
    }
}



function getSection(url, slug){
    $.get(url, function(data){
        $('#faqsection_'+slug).html(data);
    });
}
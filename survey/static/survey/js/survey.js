$("form").submit(function() {
    if($("div.checkbox-group.required :checkbox:checked").length == 0){
        $("div.checkbox-group.required").addClass("red-text");
        alert("Please answer the required questions");
        return false;
    }
});
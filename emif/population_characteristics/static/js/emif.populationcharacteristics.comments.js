/**********************************************************************
# -*- coding: utf-8 -*-
# Copyright (C) 2014 Universidade de Aveiro, DETI/IEETA, Bioinformatics Group - http://bioinformatics.ua.pt/
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

***********************************************************************/

var commentsBinded = false;
var NONCONTACTCOMMENTS = "<center>This chart does not have any associated comments. To comment please write below</center>";
function removeComment(commentId)
{

  var result = {}

  $.ajax({
    dataType: "json",
    url: "population/comments/" + commentId,
    async: false,
    data: result,
    type: "DELETE",
    success: function (data){result=data;}
  });
  $("#comment_"+ commentId).remove();

  return false;
};



function CommentsManager()
{

  var self =this;

    this.addComment = function(data) {
        if ($("#pc_comments_placeholder").text()==NONCONTACTCOMMENTS)
        {
          $("#pc_comments_placeholder").html("");
        }
        $("#pc_comments_placeholder").append('<div id="comment_'+data.id
          +'"><blockquote><p style="font-size: 16px">'+data.t_title+' <a class="delete_comment" onclick="return removeComment('+data.id+')"; " href=""><i class="icon-remove icon"></i></a></p>'
                          + '<small>'+data.description+' <br />posted on '+data.latest_date+' </small>'
                          + '</blockquote>'
                        +'</div>');
    };



    this.listComments = function(fingerprintID, chartID){
        var results = null;
        var result = {}

        $.ajax({
          dataType: "json",
          url: "population/comments/" + fingerprintID + "/" + chartID,
          async: false,
          data: result,
          success: function (data){
            result=data;
          }
        });

        if (result.length==0)
          $("#pc_comments_placeholder").html(NONCONTACTCOMMENTS);

        $.each(result, function(data)
          {
            data = result[data];

            self.addComment(data);

          });
        return result;
    };

};


$( document ).ready(function() {


    $("#pc_chart_comment_submit").on('click', function(event){

        $('#chartcomments').unbind("submit");
        $("#chartcomments").submit(function(ev){
            cm = new CommentsManager();
             var url = "population/comments"; // the script where you handle the form input.
            $.ajax({
                   type: "POST",
                   url: url,
                   data: $("#chartcomments").serialize(), // serializes the form's elements.
                   success: function(data)
                   {

                       cm.addComment(data);
                   }
                 });
            ev.preventDefault();

            return true; // avoid to execute the actual submit of the form.
            });
    });
    $("#pc_chart_comment_submit").prop('disabled', false);


});

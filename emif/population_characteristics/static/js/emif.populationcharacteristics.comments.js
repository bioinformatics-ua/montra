/**********************************************************************
# Copyright (C) 2014 Luís A. Bastião Silva and Universidade de Aveiro
#
# Authors: Luís A. Bastião Silva <bastiao@ua.pt>
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
#
***********************************************************************/

var commentsBinded = false;


$( document ).ready(function() {


    $("#pc_chart_comment_submit").on('click', function(event){

        $('#chartcomments').unbind("submit");
        $("#chartcomments").submit(function(ev){
             var url = "population/comments"; // the script where you handle the form input.
            $.ajax({
                   type: "POST",
                   url: url,
                   data: $("#chartcomments").serialize(), // serializes the form's elements.
                   success: function(data)
                   {
                       
                       $("#pc_comments_placeholder").append('<div id="comment_1"><blockquote><p style="font-size: 16px">'+data.t_title+'</p>'
                        + '<small>'+data.description+' <br />posted on '+data.latest_date+' </small>'
                        + '</blockquote>'
                      +'</div>');
                   }
                 });
            ev.preventDefault();

            return true; // avoid to execute the actual submit of the form.
            });
    });
    $("#pc_chart_comment_submit").prop('disabled', false);
});
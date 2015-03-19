/*
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
*/
function initializeBecas(pmid, container){
    var becasWidget2;

    // Initialize another widget
    becasWidget2 = new becas.Widget({
        container: container
    });
    // Request abstract annotation by PMID
    becasWidget2.annotatePublication({
        // required parameter
        pmid: pmid,
        // optional parameters
        groups: {
            "SPEC": true,
            "ANAT": true,
            "DISO": true,
            "PATH": true,
            "CHED": true,
            "ENZY": true,
            "MRNA": true,
            "PRGE": true,
            "COMP": true,
            "FUNC": true,
            "PROC": true
        },
        success: function() {
            // Everything went fine, widget is rendered.
        },
        error: function(err) {
            // An error prevented annotation, an error message has rendered.
        }
    });
}

$("#collapseall_literature").bind('click', function(e) {
    //e.preventDefault();
    //e.stopPropagation();

    collapse_expand(this);

    return false;
});

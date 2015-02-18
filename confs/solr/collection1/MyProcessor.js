/*# -*- coding: utf-8 -*-
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
#*/
//SLUG DEFINITION
var numberofpatientsslug = "number_active_patients_jan2012_d"
var numberofpatients_sort = "nrpatients_sort"

var location_slug_chain = ["city_t", "location_t", "PI:_Address_t"]
var location_sort = "location_sort"

function parseDateString(str){
  if(str == null)
  return null;

  var datePattern=new RegExp("(\\d{4})-(\\d{2})-(\\d{2}) (\\d{2}):(\\d{2}):(\\d{2})(\.(\\d+))?","");

  var parsedCreated = datePattern.exec(str);
  if(parsedCreated.length == 9){
  var ateObj = new Date(parsedCreated[1], parsedCreated[2], parsedCreated[3], parsedCreated[4], parsedCreated[5], parsedCreated[6]);
  return ateObj;
  }

  if(parsedCreated.length == 7){
      var ateObj = new Date(parsedCreated[1], parsedCreated[2], parsedCreated[3], parsedCreated[4], parsedCreated[5], parsedCreated[6]);
      return ateObj;
  }

  return null;
}

function removeNumericFieldMask(numericString){
  var number = 0;
  if(numericString != undefined && numericString.length() > 0){
    //var r = /\./g
    //var nString = numericString.replace(r, '');
    var nString = numericString.split("'").join("");
    number = parseInt(nString);
    if(number == NaN)
      return 0
  }
  return number;
}

function populateNumberOfPatientsSort(doc){
  var n = parseInt(doc.getFieldValue(numberofpatientsslug));

  if(isNaN(n)){
    n=0;
  }
  logger.info("___TIAGO___#EXTRACTED NUMBER OF PATIENTS: "+doc.getFieldValue(numberofpatientsslug));
  logger.info("___TIAGO___#REPLACED NUMBER OF PATIENTS: "+n);
  doc.setField(numberofpatients_sort, n);
}

function populateLocationSortField(doc){
  for(i in location_slug_chain){
    var value = doc.getFieldValue(location_slug_chain[i]);
    if(  value != null && value.length() > 0  ){
      doc.setField(location_sort, value);
      logger.info("___TIAGO___#SETTING LOCATION SORT: "+value);
      return ;
    }
  }
  doc.setField(location_sort, "");
}

function processAdd(cmd) {
  doc = cmd.solrDoc;  // org.apache.solr.common.SolrInputDocument 2013-10-30 14:00:32.204662
  id = doc.getFieldValue("id");
  logger.info("MyProcessor#Processing Document: id=" + id);

  var created = doc.getFieldValue("created_t");
  var date_last_mod = doc.getFieldValue("date_last_modification_t");
  var last_activ = doc.getFieldValue("last_activity_sort");
  if(last_activ != null){
     last_activ = new Date(last_activ);
  }

  var createdDate = parseDateString(created);
  var last_modDate =parseDateString(date_last_mod );

  logger.info("__TIAGO__#ADDING STUF: created0="+createdDate);
  logger.info("__TIAGO__#ADDING STUF: created0="+last_modDate);

  if(last_modDate != null && last_modDate > createdDate){
     last_activ = last_modDate.getTime();
  }else if (createdDate != null){
     last_activ = createdDate.getTime();
  }
  doc.setField("last_activity_sort", last_activ);

  logger.info("MyProcessor#ADDING Index: last_activity="+last_activ);

  populateNumberOfPatientsSort(doc);
  populateLocationSortField(doc);
// Set a field value:
//  doc.setField("foo_s", "whatever");

// Get a configuration parameter:
//  config_param = params.get('config_param');  // "params" only exists if processor configured with <lst name="params">

// Get a request parameter:
// some_param = req.getParams().get("some_param")

// Add a field of field names that match a pattern:
//   - Potentially useful to determine the fields/attributes represented in a result set, via faceting on field_name_ss
//  field_names = doc.getFieldNames().toArray();
//  for(i=0; i < field_names.length; i++) {
//    field_name = field_names[i];
//    if (/attr_.*/.test(field_name)) { doc.addField("attribute_ss", field_names[i]); }
//  }
}

function processDelete(cmd) {
  // no-op
}

function processMergeIndexes(cmd) {
  // no-op
}

function processCommit(cmd) {
  // no-op
}

function processRollback(cmd) {
  // no-op
}

function finish() {
  // no-op
}


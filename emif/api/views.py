# -*- coding: utf-8 -*-
# Copyright (C) 2013 Luís A. Bastião Silva and Universidade de Aveiro
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


from django.http import HttpResponse

from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework import permissions
from rest_framework import renderers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import json
import md5
from django.views.decorators.csrf import csrf_exempt

from rest_framework.permissions import AllowAny, IsAuthenticated

# Import Search Engine 

from searchengine.search_indexes import CoreEngine

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders it's content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@api_view(('GET','POST','OPTIONS'))

def api_root(request, format=None):
    
    return Response({
        'search': reverse('search', request=request),
        'insert': reverse('insert', request=request),
        'stats': reverse('stats', request=request),
        'validate': reverse('validate', request=request),
        
    })


class SearchView(APIView):
    def get(self, request, *args, **kw):
        # Process any get params that you may need
        # If you don't need to process get params,
        # you can skip this part
        #query = request.GET.get('query', None)

        for param in request.GET:
            print(param)
            print(request.GET.get(param))
        response = None
        #if query!=None:

        result = {'myValue': 'lol', 'myValue2': 'lol', }
        response = Response(result, status=status.HTTP_200_OK)
        #else:
        #    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return response

class AdvancedSearchView(APIView):
    def get(self, request, *args, **kw):
        # Process any get params that you may need
        # If you don't need to process get params,
        # you can skip this part
        get_arg1 = request.GET.get('arg1', None)
        get_arg2 = request.GET.get('arg2', None)

        result = {'myValue': 'lol', 'myValue2': 'lol', }
        response = Response(result, status=status.HTTP_200_OK)
        return response

class InsertView(APIView):

    def get(self, request, *args, **kw):    
        result = {'myV22222alue': 'lol', 'myValue2': 'lol' }
        response = Response(result, status=status.HTTP_200_OK)

        return response
    permission_classes = (AllowAny,)
    def post(self, request, *args, **kw):
        # Process any get params that you may need
        # If you don't need to process get params,
        # you can skip this part
        # query = request.POST.get('myValue2', None)
        # print (query)
        # print(json.loads(request.POST.get('_content')).get('myValue'))
        print request.POST
        # for param in request.POST:
        #     print(param)
        #     print(request.POST.get(param))
        #print "dasd"
        #print request.POST.items()
        #for i in request.POST.items():
        #    print i[0]
        #    json_test = json.loads(i[0])
        #    print json_test
        #data = JSONParser().parse(request)

        
        #c = CoreEngine()
        #print request.content_type
        #print request
        #print(json.loads(request.POST.get('_content')))

        #c.index_fingerprint_as_json(json.loads(request.POST.get('_content')))
        
        result = {'myValue': 'lol', 'myValue2': 'lol' }
        response = Response(result, status=status.HTTP_200_OK)

        return response


class ValidateView(APIView):
    def get(self, request, *args, **kw):    
    
        database_name = request.GET['name']
        c = CoreEngine()
        results = c.search_fingerprint("database_name_t:"+database_name)
        result = {'contains': len(results)!=0}
        
        response = Response(result, status=status.HTTP_200_OK)
        return response


    def post(self, request, *args, **kw):
        try:
            
            print request.POST.items()
            for i in request.POST.items():
                print i[0]
                json_test = json.loads(i[0])
                print json_test

            #database_name = request.POST['database_name']
            # c = CoreEngine()
            #results = c.search_fingerprint("database_name_t:"+database_name)
            #result = {'contains': len(results)==0}
            response = Response(result, status=status.HTTP_200_OK)
        except:
            print("fuck")
            raise
        return response


class StatsView(APIView):

    def get(self, request, *args, **kw):    
        result = None
        result = '{"name":"flare","children":[{"name":"analytics","children":[{"name":"cluster","children":[{"name":"AgglomerativeCluster","size":3938},{"name":"CommunityStructure","size":3812},{"name":"HierarchicalCluster","size":6714},{"name":"MergeEdge","size":743}]},{"name":"graph","children":[{"name":"BetweennessCentrality","size":3534},{"name":"LinkDistance","size":5731},{"name":"MaxFlowMinCut","size":7840},{"name":"ShortestPaths","size":5914},{"name":"SpanningTree","size":3416}]},{"name":"optimization","children":[{"name":"AspectRatioBanker","size":7074}]}]},{"name":"animate","children":[{"name":"Easing","size":17010},{"name":"FunctionSequence","size":5842},{"name":"interpolate","children":[{"name":"ArrayInterpolator","size":1983},{"name":"ColorInterpolator","size":2047},{"name":"DateInterpolator","size":1375},{"name":"Interpolator","size":8746},{"name":"MatrixInterpolator","size":2202},{"name":"NumberInterpolator","size":1382},{"name":"ObjectInterpolator","size":1629},{"name":"PointInterpolator","size":1675},{"name":"RectangleInterpolator","size":2042}]},{"name":"ISchedulable","size":1041},{"name":"Parallel","size":5176},{"name":"Pause","size":449},{"name":"Scheduler","size":5593},{"name":"Sequence","size":5534},{"name":"Transition","size":9201},{"name":"Transitioner","size":19975},{"name":"TransitionEvent","size":1116},{"name":"Tween","size":6006}]},{"name":"data","children":[{"name":"converters","children":[{"name":"Converters","size":721},{"name":"DelimitedTextConverter","size":4294},{"name":"GraphMLConverter","size":9800},{"name":"IDataConverter","size":1314},{"name":"JSONConverter","size":2220}]},{"name":"DataField","size":1759},{"name":"DataSchema","size":2165},{"name":"DataSet","size":586},{"name":"DataSource","size":3331},{"name":"DataTable","size":772},{"name":"DataUtil","size":3322}]},{"name":"display","children":[{"name":"DirtySprite","size":8833},{"name":"LineSprite","size":1732},{"name":"RectSprite","size":3623},{"name":"TextSprite","size":10066}]},{"name":"flex","children":[{"name":"FlareVis","size":4116}]},{"name":"physics","children":[{"name":"DragForce","size":1082},{"name":"GravityForce","size":1336},{"name":"IForce","size":319},{"name":"NBodyForce","size":10498},{"name":"Particle","size":2822},{"name":"Simulation","size":9983},{"name":"Spring","size":2213},{"name":"SpringForce","size":1681}]},{"name":"query","children":[{"name":"AggregateExpression","size":1616},{"name":"And","size":1027},{"name":"Arithmetic","size":3891},{"name":"Average","size":891},{"name":"BinaryExpression","size":2893},{"name":"Comparison","size":5103},{"name":"CompositeExpression","size":3677},{"name":"Count","size":781},{"name":"DateUtil","size":4141},{"name":"Distinct","size":933},{"name":"Expression","size":5130},{"name":"ExpressionIterator","size":3617},{"name":"Fn","size":3240},{"name":"If","size":2732},{"name":"IsA","size":2039},{"name":"Literal","size":1214},{"name":"Match","size":3748},{"name":"Maximum","size":843},{"name":"methods","children":[{"name":"add","size":593},{"name":"and","size":330},{"name":"average","size":287},{"name":"count","size":277},{"name":"distinct","size":292},{"name":"div","size":595},{"name":"eq","size":594},{"name":"fn","size":460},{"name":"gt","size":603},{"name":"gte","size":625},{"name":"iff","size":748},{"name":"isa","size":461},{"name":"lt","size":597},{"name":"lte","size":619},{"name":"max","size":283},{"name":"min","size":283},{"name":"mod","size":591},{"name":"mul","size":603},{"name":"neq","size":599},{"name":"not","size":386},{"name":"or","size":323},{"name":"orderby","size":307},{"name":"range","size":772},{"name":"select","size":296},{"name":"stddev","size":363},{"name":"sub","size":600},{"name":"sum","size":280},{"name":"update","size":307},{"name":"variance","size":335},{"name":"where","size":299},{"name":"xor","size":354},{"name":"_","size":264}]},{"name":"Minimum","size":843},{"name":"Not","size":1554},{"name":"Or","size":970},{"name":"Query","size":13896},{"name":"Range","size":1594},{"name":"StringUtil","size":4130},{"name":"Sum","size":791},{"name":"Variable","size":1124},{"name":"Variance","size":1876},{"name":"Xor","size":1101}]},{"name":"scale","children":[{"name":"IScaleMap","size":2105},{"name":"LinearScale","size":1316},{"name":"LogScale","size":3151},{"name":"OrdinalScale","size":3770},{"name":"QuantileScale","size":2435},{"name":"QuantitativeScale","size":4839},{"name":"RootScale","size":1756},{"name":"Scale","size":4268},{"name":"ScaleType","size":1821},{"name":"TimeScale","size":5833}]},{"name":"util","children":[{"name":"Arrays","size":8258},{"name":"Colors","size":10001},{"name":"Dates","size":8217},{"name":"Displays","size":12555},{"name":"Filter","size":2324},{"name":"Geometry","size":10993},{"name":"heap","children":[{"name":"FibonacciHeap","size":9354},{"name":"HeapNode","size":1233}]},{"name":"IEvaluable","size":335},{"name":"IPredicate","size":383},{"name":"IValueProxy","size":874},{"name":"math","children":[{"name":"DenseMatrix","size":3165},{"name":"IMatrix","size":2815},{"name":"SparseMatrix","size":3366}]},{"name":"Maths","size":17705},{"name":"Orientation","size":1486},{"name":"palette","children":[{"name":"ColorPalette","size":6367},{"name":"Palette","size":1229},{"name":"ShapePalette","size":2059},{"name":"SizePalette","size":2291}]},{"name":"Property","size":5559},{"name":"Shapes","size":19118},{"name":"Sort","size":6887},{"name":"Stats","size":6557},{"name":"Strings","size":22026}]},{"name":"vis","children":[{"name":"axis","children":[{"name":"Axes","size":1302},{"name":"Axis","size":24593},{"name":"AxisGridLine","size":652},{"name":"AxisLabel","size":636},{"name":"CartesianAxes","size":6703}]},{"name":"controls","children":[{"name":"AnchorControl","size":2138},{"name":"ClickControl","size":3824},{"name":"Control","size":1353},{"name":"ControlList","size":4665},{"name":"DragControl","size":2649},{"name":"ExpandControl","size":2832},{"name":"HoverControl","size":4896},{"name":"IControl","size":763},{"name":"PanZoomControl","size":5222},{"name":"SelectionControl","size":7862},{"name":"TooltipControl","size":8435}]},{"name":"data","children":[{"name":"Data","size":20544},{"name":"DataList","size":19788},{"name":"DataSprite","size":10349},{"name":"EdgeSprite","size":3301},{"name":"NodeSprite","size":19382},{"name":"render","children":[{"name":"ArrowType","size":698},{"name":"EdgeRenderer","size":5569},{"name":"IRenderer","size":353},{"name":"ShapeRenderer","size":2247}]},{"name":"ScaleBinding","size":11275},{"name":"Tree","size":7147},{"name":"TreeBuilder","size":9930}]},{"name":"events","children":[{"name":"DataEvent","size":2313},{"name":"SelectionEvent","size":1880},{"name":"TooltipEvent","size":1701},{"name":"VisualizationEvent","size":1117}]},{"name":"legend","children":[{"name":"Legend","size":20859},{"name":"LegendItem","size":4614},{"name":"LegendRange","size":10530}]},{"name":"operator","children":[{"name":"distortion","children":[{"name":"BifocalDistortion","size":4461},{"name":"Distortion","size":6314},{"name":"FisheyeDistortion","size":3444}]},{"name":"encoder","children":[{"name":"ColorEncoder","size":3179},{"name":"Encoder","size":4060},{"name":"PropertyEncoder","size":4138},{"name":"ShapeEncoder","size":1690},{"name":"SizeEncoder","size":1830}]},{"name":"filter","children":[{"name":"FisheyeTreeFilter","size":5219},{"name":"GraphDistanceFilter","size":3165},{"name":"VisibilityFilter","size":3509}]},{"name":"IOperator","size":1286},{"name":"label","children":[{"name":"Labeler","size":9956},{"name":"RadialLabeler","size":3899},{"name":"StackedAreaLabeler","size":3202}]},{"name":"layout","children":[{"name":"AxisLayout","size":6725},{"name":"BundledEdgeRouter","size":3727},{"name":"CircleLayout","size":9317},{"name":"CirclePackingLayout","size":12003},{"name":"DendrogramLayout","size":4853},{"name":"ForceDirectedLayout","size":8411},{"name":"IcicleTreeLayout","size":4864},{"name":"IndentedTreeLayout","size":3174},{"name":"Layout","size":7881},{"name":"NodeLinkTreeLayout","size":12870},{"name":"PieLayout","size":2728},{"name":"RadialTreeLayout","size":12348},{"name":"RandomLayout","size":870},{"name":"StackedAreaLayout","size":9121},{"name":"TreeMapLayout","size":9191}]},{"name":"Operator","size":2490},{"name":"OperatorList","size":5248},{"name":"OperatorSequence","size":4190},{"name":"OperatorSwitch","size":2581},{"name":"SortOperator","size":2023}]},{"name":"Visualization","size":16540}]}]}'
        result = '{"charttype": "piechart" , "attr1": "name" , "attr2": "score" ,"charts": [{"name":"3", "score":180}, {"name":"3dsad", "score":180}]}'
        result = json.loads(result)
        response = Response(result, status=status.HTTP_200_OK)

        return response
    
import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_Utility as AllplanUtil
import GeometryValidate as GeometryValidate
from HandleDirection import HandleDirection
from HandleProperties import HandleProperties


def check_allplan_version(el_build, version):
    del el_build
    del version
    return True


def create_element(el_build, doc):
    element = Beam(doc)
    return element.create(el_build)


class Beam:
    def __init__(self, doc):
        self.model_el_b = []
        self.ruchka = []
        self.document = doc

    def connect_all_parts(self, el_build):
        com_prop = AllplanBaseElements.CommonProperties()
        com_prop.GetGlobalProperties()
        com_prop.Pen = 1
        com_prop.Color = 3
        com_prop.Stroke = 1
        polyhedron_bottom = self.create_lower_part_beam(el_build)
        polyhedron_center = self.create_central_part_beam(el_build)
        polyhedron_top = self.create_top_part_beam(el_build)
        err, polyhedron = AllplanGeo.MakeUnion(polyhedron_bottom, polyhedron_center)
        if err:
            return
        err, polyhedron = AllplanGeo.MakeUnion(polyhedron, polyhedron_top)
        if err:
            return 
        self.model_el_b.append(
            AllplanBasisElements.ModelElement3D(com_prop, polyhedron))
    def create(self, el_build):
        self.connect_all_parts(el_build)
        self.create_lower_part_beam(el_build)
        return (self.model_el_b, self.ruchka)

    # must be updated
    def create_lower_part_beam(self, el_build):
        polyhedron = self.lower_part_addiction_1(el_build)
        err, polyhedron = AllplanGeo.MakeUnion(polyhedron, self.lower_part_addiction_2(el_build))      
        err, polyhedron = AllplanGeo.MakeUnion(polyhedron, self.lower_part_addiction_2_2(el_build))    
        err, polyhedron = AllplanGeo.MakeUnion(polyhedron, self.lower_part_addiction_2_3(el_build))
        err, polyhedron = AllplanGeo.MakeUnion(polyhedron, self.lower_part_addiction_2_4(el_build))
        err, polyhedron = AllplanGeo.MakeUnion(polyhedron, self.lower_part_addiction_3(el_build))
        err, polyhedron = AllplanGeo.MakeUnion(polyhedron, self.lower_part_addiction_3_2(el_build))
        err, polyhedron = AllplanGeo.MakeUnion(polyhedron, self.lower_part_addiction_3_3(el_build))
        err, polyhedron = AllplanGeo.MakeUnion(polyhedron, self.lower_part_addiction_3_4(el_build))
        err, polyhedron = AllplanGeo.MakeUnion(polyhedron, self.lower_part_addiction_4(el_build))
        err, polyhedron = AllplanGeo.MakeUnion(polyhedron, self.lower_part_addiction_4_2(el_build))
        err, polyhedron = AllplanGeo.MakeUnion(polyhedron, self.last_lower_part(el_build))
        return polyhedron

    def create_central_part_beam(self, el_build):
        base_pol = AllplanGeo.Polygon3D()
        base_pol += AllplanGeo.Point3D(0, el_build.LengthBottomCut.value, el_build.HeightBottom.value)
        base_pol += AllplanGeo.Point3D(0, el_build.WidthBottom.value - el_build.LengthBottomCut.value, el_build.HeightBottom.value)
        base_pol += AllplanGeo.Point3D(el_build.LengthCenterWidth.value, el_build.WidthBottom.value - el_build.LengthBottomCut.value, el_build.HeightBottom.value)
        base_pol += AllplanGeo.Point3D(el_build.LengthCenterWidth.value + el_build.LengthTransition.value, 
                                        el_build.WidthBottom.value - el_build.LengthBottomCut.value - (el_build.WidthBottom.value - el_build.LengthBottomCut.value * 2 - el_build.WidthCentralLittle.value) / 2, 
                                        el_build.HeightBottom.value)
        base_pol += AllplanGeo.Point3D(el_build.Length.value - (el_build.LengthCenterWidth.value + el_build.LengthTransition.value), 
                                        el_build.WidthBottom.value - el_build.LengthBottomCut.value - (el_build.WidthBottom.value - el_build.LengthBottomCut.value * 2 - el_build.WidthCentralLittle.value) / 2, 
                                        el_build.HeightBottom.value)
        base_pol += AllplanGeo.Point3D(el_build.Length.value - el_build.LengthCenterWidth.value,
                                         el_build.WidthBottom.value - el_build.LengthBottomCut.value, 
                                         el_build.HeightBottom.value)
        base_pol += AllplanGeo.Point3D(el_build.Length.value, el_build.WidthBottom.value - el_build.LengthBottomCut.value, el_build.HeightBottom.value)
        base_pol += AllplanGeo.Point3D(el_build.Length.value, el_build.LengthBottomCut.value, el_build.HeightBottom.value)
        base_pol += AllplanGeo.Point3D(el_build.Length.value - el_build.LengthCenterWidth.value, el_build.LengthBottomCut.value, el_build.HeightBottom.value)
        base_pol += AllplanGeo.Point3D(el_build.Length.value - el_build.LengthCenterWidth.value - el_build.LengthTransition.value,
                                        el_build.LengthBottomCut.value + (el_build.WidthBottom.value - el_build.LengthBottomCut.value * 2 - el_build.WidthCentralLittle.value) / 2, 
                                        el_build.HeightBottom.value)
        base_pol += AllplanGeo.Point3D(el_build.LengthCenterWidth.value + el_build.LengthTransition.value,
                                        el_build.LengthBottomCut.value + (el_build.WidthBottom.value - el_build.LengthBottomCut.value * 2 - el_build.WidthCentralLittle.value) / 2, 
                                        el_build.HeightBottom.value)
        base_pol += AllplanGeo.Point3D(el_build.LengthCenterWidth.value,
                                        el_build.LengthBottomCut.value, 
                                        el_build.HeightBottom.value)
        base_pol += AllplanGeo.Point3D(0, el_build.LengthBottomCut.value, el_build.HeightBottom.value)


        path = AllplanGeo.Polyline3D()
        path += AllplanGeo.Point3D(0, el_build.LengthBottomCut.value, el_build.HeightBottom.value)
        path += AllplanGeo.Point3D(0, el_build.LengthBottomCut.value, el_build.HeightBottom.value + el_build.HeightCenter.value)

        err, polyhedron = AllplanGeo.CreatePolyhedron(base_pol, path)

        if err:
            return []

        return polyhedron

    def create_top_part_beam(self, el_build):
        polyhedron = self.top_part_addiction_1(el_build)
        
        err, polyhedron = AllplanGeo.MakeUnion(polyhedron, self.top_part_addiction_2(el_build))
        err, polyhedron = AllplanGeo.MakeUnion(polyhedron, self.top_part_addiction_2_2(el_build))
        err, polyhedron = AllplanGeo.MakeUnion(polyhedron, self.top_part_addiction_2_3(el_build))
        err, polyhedron = AllplanGeo.MakeUnion(polyhedron, self.top_part_addiction_3(el_build))
        err, polyhedron = AllplanGeo.MakeUnion(polyhedron, self.top_part_addiction_3(el_build, plus=(el_build.Length.value - el_build.LengthCenterWidth.value)))
        err, polyhedron = AllplanGeo.MakeUnion(polyhedron, self.top_part_addiction_3_3(el_build))
        err, polyhedron = AllplanGeo.MakeUnion(polyhedron, self.top_part_addiction_4(el_build))
        err, polyhedron = AllplanGeo.MakeUnion(polyhedron, self.top_part_addiction_4(el_build, el_build.WidthBottom.value - el_build.LengthBottomCut.value * 2, el_build.WidthTop.value, 10))
        err, polyhedron = AllplanGeo.MakeUnion(polyhedron, self.top_part_addiction_4_2(el_build))
        err, polyhedron = AllplanGeo.MakeUnion(polyhedron, self.top_part_addiction_4_2(el_build, el_build.WidthBottom.value - el_build.LengthBottomCut.value * 2, el_build.WidthTop.value, 10))   
        err, polyhedron = AllplanGeo.MakeUnion(polyhedron, self.last_top_part(el_build))
        return polyhedron

    def top_part_addiction_1(self, el_build):
        base_pol = AllplanGeo.Polygon3D()
        base_pol += AllplanGeo.Point3D(el_build.LengthCenterWidth.value, 
                                        el_build.WidthBottom.value - el_build.LengthBottomCut.value - (el_build.WidthBottom.value - el_build.LengthBottomCut.value * 2 - el_build.WidthCentralLittle.value) / 2,
                                        el_build.HeightBottom.value + el_build.HeightCenter.value)
        base_pol += AllplanGeo.Point3D(el_build.LengthCenterWidth.value, 
                                        el_build.WidthTop.value - (el_build.WidthTop.value - el_build.WidthBottom.value) / 2,
                                        el_build.HeightBottom.value + el_build.HeightCenter.value + el_build.HeightTopCut.value)
        base_pol += AllplanGeo.Point3D(el_build.LengthCenterWidth.value, 
                                        -(el_build.WidthTop.value - el_build.WidthBottom.value) / 2,
                                        el_build.HeightBottom.value + el_build.HeightCenter.value + el_build.HeightTopCut.value)
        base_pol += AllplanGeo.Point3D(el_build.LengthCenterWidth.value, 
                                        el_build.LengthBottomCut.value + (el_build.WidthBottom.value - el_build.LengthBottomCut.value * 2 - el_build.WidthCentralLittle.value) / 2,
                                        el_build.HeightBottom.value + el_build.HeightCenter.value)
        base_pol += AllplanGeo.Point3D(el_build.LengthCenterWidth.value, 
                                        el_build.WidthBottom.value - el_build.LengthBottomCut.value - (el_build.WidthBottom.value - el_build.LengthBottomCut.value * 2 - el_build.WidthCentralLittle.value) / 2,
                                        el_build.HeightBottom.value + el_build.HeightCenter.value)
        path = AllplanGeo.Polyline3D()
        path += AllplanGeo.Point3D(el_build.LengthCenterWidth.value, 
                                        el_build.WidthBottom.value - el_build.LengthBottomCut.value - (el_build.WidthBottom.value - el_build.LengthBottomCut.value * 2 - el_build.WidthCentralLittle.value) / 2,
                                        el_build.HeightBottom.value + el_build.HeightCenter.value)
        path += AllplanGeo.Point3D(el_build.Length.value - el_build.LengthCenterWidth.value, 
                                        el_build.WidthBottom.value - el_build.LengthBottomCut.value - (el_build.WidthBottom.value - el_build.LengthBottomCut.value * 2 - el_build.WidthCentralLittle.value) / 2,
                                        el_build.HeightBottom.value + el_build.HeightCenter.value)
        
        err, polyhedron = AllplanGeo.CreatePolyhedron(base_pol, path)

        if err:
            return []

        return polyhedron

    def top_part_addiction_2(self, el_build):
        base_pol = AllplanGeo.Polygon3D()
        base_pol += AllplanGeo.Point3D(el_build.Length.value - el_build.LengthCenterWidth.value, el_build.WidthBottom.value - el_build.LengthBottomCut.value, el_build.HeightBottom.value + el_build.HeightCenter.value)
        base_pol += AllplanGeo.Point3D(el_build.Length.value - el_build.LengthCenterWidth.value - el_build.LengthTransition.value, el_build.WidthBottom.value - el_build.LengthBottomCut.value - (el_build.WidthBottom.value - el_build.LengthBottomCut.value * 2 - el_build.WidthCentralLittle.value) / 2 , el_build.HeightBottom.value + el_build.HeightCenter.value)
        base_pol += AllplanGeo.Point3D(el_build.Length.value - el_build.LengthCenterWidth.value - el_build.LengthTransition.value - (el_build.WidthBottom.value - el_build.LengthBottomCut.value * 2 - el_build.WidthCentralLittle.value) / 2 , el_build.WidthBottom.value - (el_build.WidthBottom.value - el_build.LengthBottomCut.value * 2 - el_build.WidthCentralLittle.value) / 2 + (el_build.WidthTop.value - el_build.WidthBottom.value) / 2, el_build.HeightBottom.value + el_build.HeightCenter.value + el_build.HeightTopCut.value)
        base_pol += AllplanGeo.Point3D(el_build.Length.value - el_build.LengthCenterWidth.value - (el_build.WidthBottom.value - el_build.LengthBottomCut.value * 2 - el_build.WidthCentralLittle.value) / 2, el_build.WidthBottom.value + (el_build.WidthTop.value - el_build.WidthBottom.value) / 2, el_build.HeightBottom.value + el_build.HeightCenter.value + el_build.HeightTopCut.value)
        base_pol += AllplanGeo.Point3D(el_build.Length.value - el_build.LengthCenterWidth.value, el_build.WidthBottom.value - el_build.LengthBottomCut.value, el_build.HeightBottom.value + el_build.HeightCenter.value)


        path = AllplanGeo.Polyline3D()
        path += AllplanGeo.Point3D(el_build.Length.value - el_build.LengthCenterWidth.value, el_build.WidthBottom.value - el_build.LengthBottomCut.value, el_build.HeightBottom.value + el_build.HeightCenter.value)
        path += AllplanGeo.Point3D(el_build.Length.value - el_build.LengthCenterWidth.value + 10, el_build.WidthBottom.value - el_build.LengthBottomCut.value - 10, el_build.HeightBottom.value + el_build.HeightCenter.value + 10)

        err, polyhedron = AllplanGeo.CreatePolyhedron(base_pol, path)
   
        if err:
            return []

        return polyhedron

    def top_part_addiction_3(self, el_build, plus=0):
        base_pol = AllplanGeo.Polygon3D()
        base_pol += AllplanGeo.Point3D(plus, el_build.LengthBottomCut.value, el_build.HeightBottom.value + el_build.HeightCenter.value)
        base_pol += AllplanGeo.Point3D(plus, el_build.WidthBottom.value - el_build.LengthBottomCut.value, el_build.HeightBottom.value + el_build.HeightCenter.value)
        base_pol += AllplanGeo.Point3D(plus, el_build.WidthBottom.value + (el_build.WidthTop.value - el_build.WidthBottom.value) / 2, el_build.HeightBottom.value + el_build.HeightCenter.value + el_build.HeightTopCut.value)
        base_pol += AllplanGeo.Point3D(plus, -(el_build.WidthTop.value - el_build.WidthBottom.value) / 2, el_build.HeightBottom.value + el_build.HeightCenter.value + el_build.HeightTopCut.value)
        base_pol += AllplanGeo.Point3D(plus, el_build.LengthBottomCut.value, el_build.HeightBottom.value + el_build.HeightCenter.value)
        path = AllplanGeo.Polyline3D()
        path += AllplanGeo.Point3D(plus, el_build.LengthBottomCut.value, el_build.HeightBottom.value + el_build.HeightCenter.value)
        path += AllplanGeo.Point3D(plus + el_build.LengthCenterWidth.value, el_build.LengthBottomCut.value, el_build.HeightBottom.value + el_build.HeightCenter.value)

        err, polyhedron = AllplanGeo.CreatePolyhedron(base_pol, path)
    
        if err:
            return []

        return polyhedron

    def top_part_addiction_4(self, el_build, minus_1 = 0, minus_2 = 0, digit = -10):
        base_pol = AllplanGeo.Polygon3D()
        base_pol += AllplanGeo.Point3D(el_build.Length.value - el_build.LengthCenterWidth.value, el_build.WidthBottom.value - el_build.LengthBottomCut.value - minus_1, el_build.HeightBottom.value + el_build.HeightCenter.value)
        base_pol += AllplanGeo.Point3D(el_build.Length.value - el_build.LengthCenterWidth.value, el_build.WidthTop.value - (el_build.WidthTop.value - el_build.WidthBottom.value) / 2 - minus_2, el_build.HeightBottom.value + el_build.HeightCenter.value + el_build.HeightTopCut.value)
        base_pol += AllplanGeo.Point3D(el_build.Length.value - el_build.LengthCenterWidth.value - (el_build.WidthBottom.value - el_build.LengthBottomCut.value * 2 - el_build.WidthCentralLittle.value) / 2, el_build.WidthBottom.value + (el_build.WidthTop.value - el_build.WidthBottom.value) / 2 - minus_2, el_build.HeightBottom.value + el_build.HeightCenter.value + el_build.HeightTopCut.value)
        base_pol += AllplanGeo.Point3D(el_build.Length.value - el_build.LengthCenterWidth.value, el_build.WidthBottom.value - el_build.LengthBottomCut.value - minus_1, el_build.HeightBottom.value + el_build.HeightCenter.value)
        path = AllplanGeo.Polyline3D()
        path += AllplanGeo.Point3D(el_build.Length.value - el_build.LengthCenterWidth.value, el_build.WidthBottom.value - el_build.LengthBottomCut.value - minus_1, el_build.HeightBottom.value + el_build.HeightCenter.value)
        path += AllplanGeo.Point3D(el_build.Length.value - el_build.LengthCenterWidth.value, el_build.WidthBottom.value - el_build.LengthBottomCut.value + digit - minus_1, el_build.HeightBottom.value + el_build.HeightCenter.value)
        print(base_pol)
        print(path)
        err, polyhedron = AllplanGeo.CreatePolyhedron(base_pol, path)
      
        if err:
            return []

        return polyhedron

    def top_part_addiction_2_2(self, el_build):
        base_pol = AllplanGeo.Polygon3D()
        base_pol += AllplanGeo.Point3D(el_build.Length.value - el_build.LengthCenterWidth.value, el_build.LengthBottomCut.value, el_build.HeightBottom.value + el_build.HeightCenter.value)
        base_pol += AllplanGeo.Point3D(el_build.Length.value - el_build.LengthCenterWidth.value - el_build.LengthTransition.value, el_build.LengthBottomCut.value + (el_build.WidthBottom.value - el_build.LengthBottomCut.value * 2 - el_build.WidthCentralLittle.value) / 2, el_build.HeightBottom.value + el_build.HeightCenter.value)
        base_pol += AllplanGeo.Point3D(el_build.Length.value - el_build.LengthCenterWidth.value - el_build.LengthTransition.value - (el_build.WidthBottom.value - el_build.LengthBottomCut.value * 2 - el_build.WidthCentralLittle.value) / 2, (el_build.WidthBottom.value - el_build.LengthBottomCut.value * 2 - el_build.WidthCentralLittle.value) / 2 - (el_build.WidthTop.value - el_build.WidthBottom.value) / 2, el_build.HeightBottom.value + el_build.HeightCenter.value + el_build.HeightTopCut.value)
        base_pol += AllplanGeo.Point3D(el_build.Length.value - el_build.LengthCenterWidth.value - (el_build.WidthBottom.value - el_build.LengthBottomCut.value * 2 - el_build.WidthCentralLittle.value) / 2, -(el_build.WidthTop.value - el_build.WidthBottom.value) / 2, el_build.HeightBottom.value + el_build.HeightCenter.value + el_build.HeightTopCut.value)
        base_pol += AllplanGeo.Point3D(el_build.Length.value - el_build.LengthCenterWidth.value, el_build.LengthBottomCut.value, el_build.HeightBottom.value + el_build.HeightCenter.value)
        path = AllplanGeo.Polyline3D()
        path += AllplanGeo.Point3D(el_build.Length.value - el_build.LengthCenterWidth.value, el_build.LengthBottomCut.value, el_build.HeightBottom.value + el_build.HeightCenter.value)
        path += AllplanGeo.Point3D(el_build.Length.value - el_build.LengthCenterWidth.value + 10, el_build.LengthBottomCut.value + 10, el_build.HeightBottom.value + el_build.HeightCenter.value + 10)

        err, polyhedron = AllplanGeo.CreatePolyhedron(base_pol, path)

        
        if err:
            return []

        return polyhedron

    def top_part_addiction_2_3(self, el_build):
        base_pol = AllplanGeo.Polygon3D()
        base_pol += AllplanGeo.Point3D(el_build.LengthCenterWidth.value, el_build.WidthBottom.value - el_build.LengthBottomCut.value, el_build.HeightBottom.value + el_build.HeightCenter.value)
        base_pol += AllplanGeo.Point3D(el_build.LengthCenterWidth.value + el_build.LengthTransition.value, el_build.WidthBottom.value - el_build.LengthBottomCut.value - (el_build.WidthBottom.value - el_build.LengthBottomCut.value * 2 - el_build.WidthCentralLittle.value) / 2, el_build.HeightBottom.value + el_build.HeightCenter.value)
        base_pol += AllplanGeo.Point3D(el_build.LengthCenterWidth.value + el_build.LengthTransition.value + (el_build.WidthBottom.value - el_build.LengthBottomCut.value * 2 - el_build.WidthCentralLittle.value) / 2, el_build.WidthBottom.value - (el_build.WidthBottom.value - el_build.LengthBottomCut.value * 2 - el_build.WidthCentralLittle.value) / 2 + (el_build.WidthTop.value - el_build.WidthBottom.value) / 2, el_build.HeightBottom.value + el_build.HeightCenter.value + el_build.HeightTopCut.value)
        base_pol += AllplanGeo.Point3D(el_build.LengthCenterWidth.value + (el_build.WidthBottom.value - el_build.LengthBottomCut.value * 2 - el_build.WidthCentralLittle.value) / 2, el_build.WidthBottom.value + (el_build.WidthTop.value - el_build.WidthBottom.value) / 2, el_build.HeightBottom.value + el_build.HeightCenter.value + el_build.HeightTopCut.value)
        base_pol += AllplanGeo.Point3D(el_build.LengthCenterWidth.value, el_build.WidthBottom.value - el_build.LengthBottomCut.value, el_build.HeightBottom.value + el_build.HeightCenter.value)
        path = AllplanGeo.Polyline3D()
        path += AllplanGeo.Point3D(el_build.LengthCenterWidth.value, el_build.WidthBottom.value - el_build.LengthBottomCut.value, el_build.HeightBottom.value + el_build.HeightCenter.value)
        path += AllplanGeo.Point3D(el_build.LengthCenterWidth.value - 10, el_build.WidthBottom.value - el_build.LengthBottomCut.value - 10, el_build.HeightBottom.value + el_build.HeightCenter.value - 10)
        err, polyhedron = AllplanGeo.CreatePolyhedron(base_pol, path)
    
        if err:
            return []

        return polyhedron

    def top_part_addiction_4_2(self, el_build, minus_1 = 0, minus_2 = 0, digit = -10):
        base_pol = AllplanGeo.Polygon3D()
        base_pol += AllplanGeo.Point3D(el_build.LengthCenterWidth.value, el_build.WidthBottom.value - el_build.LengthBottomCut.value - minus_1, el_build.HeightBottom.value + el_build.HeightCenter.value)
        base_pol += AllplanGeo.Point3D(el_build.LengthCenterWidth.value, el_build.WidthBottom.value + (el_build.WidthTop.value - el_build.WidthBottom.value) / 2 - minus_2, el_build.HeightBottom.value + el_build.HeightCenter.value + el_build.HeightTopCut.value)
        base_pol += AllplanGeo.Point3D(el_build.LengthCenterWidth.value + (el_build.WidthBottom.value - el_build.LengthBottomCut.value * 2 - el_build.WidthCentralLittle.value) / 2, el_build.WidthBottom.value + (el_build.WidthTop.value - el_build.WidthBottom.value) / 2 - minus_2, el_build.HeightBottom.value + el_build.HeightCenter.value + el_build.HeightTopCut.value)
        base_pol += AllplanGeo.Point3D(el_build.LengthCenterWidth.value, el_build.WidthBottom.value - el_build.LengthBottomCut.value - minus_1, el_build.HeightBottom.value + el_build.HeightCenter.value)  
        path = AllplanGeo.Polyline3D()
        path += AllplanGeo.Point3D(el_build.LengthCenterWidth.value, el_build.WidthBottom.value - el_build.LengthBottomCut.value - minus_1, el_build.HeightBottom.value + el_build.HeightCenter.value)
        path += AllplanGeo.Point3D(el_build.LengthCenterWidth.value, el_build.WidthBottom.value - el_build.LengthBottomCut.value - minus_1 + digit, el_build.HeightBottom.value + el_build.HeightCenter.value)

        err, polyhedron = AllplanGeo.CreatePolyhedron(base_pol, path)

        if err:
            return []

        return polyhedron

    def top_part_addiction_3_3(self, el_build):
        base_pol = AllplanGeo.Polygon3D()
        base_pol += AllplanGeo.Point3D(el_build.LengthCenterWidth.value, el_build.LengthBottomCut.value, el_build.HeightBottom.value + el_build.HeightCenter.value)
        base_pol += AllplanGeo.Point3D(el_build.LengthCenterWidth.value + el_build.LengthTransition.value, el_build.LengthBottomCut.value + (el_build.WidthBottom.value - el_build.LengthBottomCut.value * 2 - el_build.WidthCentralLittle.value) / 2, el_build.HeightBottom.value + el_build.HeightCenter.value)
        base_pol += AllplanGeo.Point3D(el_build.LengthCenterWidth.value + el_build.LengthTransition.value + (el_build.WidthBottom.value - el_build.LengthBottomCut.value * 2 - el_build.WidthCentralLittle.value) / 2, (el_build.WidthBottom.value - el_build.LengthBottomCut.value * 2 - el_build.WidthCentralLittle.value) / 2 - (el_build.WidthTop.value - el_build.WidthBottom.value) / 2, el_build.HeightBottom.value + el_build.HeightCenter.value + el_build.HeightTopCut.value)
        base_pol += AllplanGeo.Point3D(el_build.LengthCenterWidth.value + (el_build.WidthBottom.value - el_build.LengthBottomCut.value * 2 - el_build.WidthCentralLittle.value) / 2, -(el_build.WidthTop.value - el_build.WidthBottom.value) / 2, el_build.HeightBottom.value + el_build.HeightCenter.value + el_build.HeightTopCut.value)
        base_pol += AllplanGeo.Point3D(el_build.LengthCenterWidth.value, el_build.LengthBottomCut.value, el_build.HeightBottom.value + el_build.HeightCenter.value)
        path = AllplanGeo.Polyline3D()
        path += AllplanGeo.Point3D(el_build.LengthCenterWidth.value, el_build.LengthBottomCut.value, el_build.HeightBottom.value + el_build.HeightCenter.value)
        path += AllplanGeo.Point3D(el_build.LengthCenterWidth.value - 10, el_build.LengthBottomCut.value + 10, el_build.HeightBottom.value + el_build.HeightCenter.value - 10)

        err, polyhedron = AllplanGeo.CreatePolyhedron(base_pol, path)
 
        if err:
            return []

        return polyhedron

    def last_top_part(self, el_build):
        base_pol = AllplanGeo.Polygon3D()
        base_pol += AllplanGeo.Point3D(0, -(el_build.WidthTop.value - el_build.WidthBottom.value) / 2, el_build.HeightBottom.value + el_build.HeightCenter.value + el_build.HeightTopCut.value)
        base_pol += AllplanGeo.Point3D(0, el_build.WidthTop.value - (el_build.WidthTop.value - el_build.WidthBottom.value) / 2, el_build.HeightBottom.value + el_build.HeightCenter.value + el_build.HeightTopCut.value)
        base_pol += AllplanGeo.Point3D(0, el_build.WidthTop.value - (el_build.WidthTop.value - el_build.WidthBottom.value) / 2, el_build.HeightBottom.value + el_build.HeightCenter.value + el_build.HeightTop.value)
        base_pol += AllplanGeo.Point3D(0, el_build.WidthTop.value - (el_build.WidthTop.value - el_build.WidthBottom.value) / 2 - el_build.Identation.value, el_build.HeightBottom.value + el_build.HeightCenter.value + el_build.HeightTop.value)
        base_pol += AllplanGeo.Point3D(0, el_build.WidthTop.value - (el_build.WidthTop.value - el_build.WidthBottom.value) / 2 - el_build.Identation.value, el_build.HeightBottom.value + el_build.HeightCenter.value + el_build.HeightTop.value + el_build.HeightPlate.value)
        base_pol += AllplanGeo.Point3D(0, - (el_build.WidthTop.value - el_build.WidthBottom.value) / 2 + el_build.Identation.value, el_build.HeightBottom.value + el_build.HeightCenter.value + el_build.HeightTop.value + el_build.HeightPlate.value)
        base_pol += AllplanGeo.Point3D(0, - (el_build.WidthTop.value - el_build.WidthBottom.value) / 2 + el_build.Identation.value, el_build.HeightBottom.value + el_build.HeightCenter.value + el_build.HeightTop.value)
        base_pol += AllplanGeo.Point3D(0, - (el_build.WidthTop.value - el_build.WidthBottom.value) / 2, el_build.HeightBottom.value + el_build.HeightCenter.value + el_build.HeightTop.value)
        base_pol += AllplanGeo.Point3D(0, -(el_build.WidthTop.value - el_build.WidthBottom.value) / 2, el_build.HeightBottom.value + el_build.HeightCenter.value + el_build.HeightTopCut.value)
        path = AllplanGeo.Polyline3D()
        path += AllplanGeo.Point3D(0, -(el_build.WidthTop.value - el_build.WidthBottom.value) / 2, el_build.HeightBottom.value + el_build.HeightCenter.value + el_build.HeightTopCut.value)
        path += AllplanGeo.Point3D(el_build.Length.value, -(el_build.WidthTop.value - el_build.WidthBottom.value) / 2, el_build.HeightBottom.value + el_build.HeightCenter.value + el_build.HeightTopCut.value)
        err, polyhedron = AllplanGeo.CreatePolyhedron(base_pol, path)
   
        if err:
            return []
        return polyhedron

    def lower_part_addiction_1(self, el_build):
        base_pol = AllplanGeo.Polygon3D()
        base_pol += AllplanGeo.Point3D(el_build.LengthCenterWidth.value, el_build.WidthBottom.value, el_build.HeightBottom.value - el_build.HeightBottomCut.value)
        base_pol += AllplanGeo.Point3D(el_build.LengthCenterWidth.value, 
                                    el_build.WidthBottom.value - el_build.LengthBottomCut.value - (el_build.WidthBottom.value - el_build.LengthBottomCut.value * 2 - el_build.WidthCentralLittle.value) / 2,
                                    el_build.HeightBottom.value)
        base_pol += AllplanGeo.Point3D(el_build.LengthCenterWidth.value, 
                                    el_build.WidthBottom.value - el_build.LengthBottomCut.value - (el_build.WidthBottom.value - el_build.LengthBottomCut.value * 2 - el_build.WidthCentralLittle.value) / 2 - el_build.WidthCentralLittle.value,
                                    el_build.HeightBottom.value)
        base_pol += AllplanGeo.Point3D(el_build.LengthCenterWidth.value, 0, el_build.HeightBottom.value - el_build.HeightBottomCut.value)
        base_pol += AllplanGeo.Point3D(el_build.LengthCenterWidth.value, el_build.WidthBottom.value, el_build.HeightBottom.value - el_build.HeightBottomCut.value)
        path = AllplanGeo.Polyline3D()
        path += AllplanGeo.Point3D(el_build.LengthCenterWidth.value, el_build.WidthBottom.value, el_build.HeightBottom.value - el_build.HeightBottomCut.value)
        path += AllplanGeo.Point3D(el_build.Length.value - el_build.LengthCenterWidth.value, el_build.WidthBottom.value, el_build.HeightBottom.value - el_build.HeightBottomCut.value)
        err, polyhedron = AllplanGeo.CreatePolyhedron(base_pol, path)

        if err:
            return []

        return polyhedron
    
    def lower_part_addiction_2(self, el_build):
        base_pol = AllplanGeo.Polygon3D()
        base_pol += AllplanGeo.Point3D(el_build.LengthCenterWidth.value, el_build.WidthBottom.value - el_build.LengthBottomCut.value, el_build.HeightBottom.value)
        base_pol += AllplanGeo.Point3D(el_build.LengthCenterWidth.value + el_build.LengthTransition.value, el_build.WidthBottom.value - el_build.LengthBottomCut.value - (el_build.WidthBottom.value - el_build.LengthBottomCut.value * 2 - el_build.WidthCentralLittle.value) / 2, el_build.HeightBottom.value)
        base_pol += AllplanGeo.Point3D(el_build.LengthCenterWidth.value + el_build.LengthTransition.value + (el_build.WidthBottom.value - el_build.LengthBottomCut.value * 2 - el_build.WidthCentralLittle.value) / 2, el_build.WidthBottom.value - (el_build.WidthBottom.value - el_build.LengthBottomCut.value * 2 - el_build.WidthCentralLittle.value) / 2, el_build.HeightBottom.value - el_build.HeightBottomCut.value)
        base_pol += AllplanGeo.Point3D(el_build.LengthCenterWidth.value + (el_build.WidthBottom.value - el_build.LengthBottomCut.value * 2 - el_build.WidthCentralLittle.value) / 2, el_build.WidthBottom.value, el_build.HeightBottom.value - el_build.HeightBottomCut.value)
        base_pol += AllplanGeo.Point3D(el_build.LengthCenterWidth.value, el_build.WidthBottom.value - el_build.LengthBottomCut.value, el_build.HeightBottom.value)
        path = AllplanGeo.Polyline3D()
        path += AllplanGeo.Point3D(el_build.LengthCenterWidth.value, el_build.WidthBottom.value - el_build.LengthBottomCut.value, el_build.HeightBottom.value)
        path += AllplanGeo.Point3D(el_build.LengthCenterWidth.value - 10 , el_build.WidthBottom.value - el_build.LengthBottomCut.value - 10, el_build.HeightBottom.value - 10)

        err, polyhedron = AllplanGeo.CreatePolyhedron(base_pol, path)
       
        if err:
            return []

        return polyhedron

    def lower_part_addiction_3(self, el_build):
        base_pol = AllplanGeo.Polygon3D()
        base_pol += AllplanGeo.Point3D(0, el_build.WidthBottom.value, el_build.HeightBottom.value - el_build.HeightBottomCut.value)
        base_pol += AllplanGeo.Point3D(0, el_build.WidthBottom.value - el_build.LengthBottomCut.value, el_build.HeightBottom.value)
        base_pol += AllplanGeo.Point3D(0, el_build.LengthBottomCut.value, el_build.HeightBottom.value)
        base_pol += AllplanGeo.Point3D(0, 0, el_build.HeightBottom.value - el_build.HeightBottomCut.value)
        base_pol += AllplanGeo.Point3D(0, el_build.WidthBottom.value, el_build.HeightBottom.value - el_build.HeightBottomCut.value)
        path = AllplanGeo.Polyline3D()
        path += AllplanGeo.Point3D(0, el_build.WidthBottom.value, el_build.HeightBottom.value - el_build.HeightBottomCut.value)
        path += AllplanGeo.Point3D(el_build.LengthCenterWidth.value, el_build.WidthBottom.value, el_build.HeightBottom.value - el_build.HeightBottomCut.value)

        err, polyhedron = AllplanGeo.CreatePolyhedron(base_pol, path)
  
        if err:
            return []

        return polyhedron

    def lower_part_addiction_4(self, el_build):
        base_pol = AllplanGeo.Polygon3D()
        base_pol += AllplanGeo.Point3D(el_build.LengthCenterWidth.value, el_build.WidthBottom.value - el_build.LengthBottomCut.value, el_build.HeightBottom.value)
        base_pol += AllplanGeo.Point3D(el_build.LengthCenterWidth.value, el_build.WidthBottom.value, el_build.HeightBottom.value - el_build.HeightBottomCut.value)
        base_pol += AllplanGeo.Point3D(el_build.LengthCenterWidth.value + (el_build.WidthBottom.value - el_build.LengthBottomCut.value * 2 - el_build.WidthCentralLittle.value) / 2, el_build.WidthBottom.value, el_build.HeightBottom.value - el_build.HeightBottomCut.value)
        base_pol += AllplanGeo.Point3D(el_build.LengthCenterWidth.value, el_build.WidthBottom.value - el_build.LengthBottomCut.value, el_build.HeightBottom.value)   
        path = AllplanGeo.Polyline3D()
        path += AllplanGeo.Point3D(el_build.LengthCenterWidth.value, el_build.WidthBottom.value - el_build.LengthBottomCut.value, el_build.HeightBottom.value)
        path += AllplanGeo.Point3D(el_build.LengthCenterWidth.value, el_build.WidthBottom.value - el_build.LengthBottomCut.value - 10, el_build.HeightBottom.value)

        err, polyhedron = AllplanGeo.CreatePolyhedron(base_pol, path)

        if err:
            return []

        return polyhedron

    def lower_part_addiction_2_2(self, el_build):
        base_pol = AllplanGeo.Polygon3D()
        base_pol += AllplanGeo.Point3D(el_build.LengthCenterWidth.value, el_build.LengthBottomCut.value, el_build.HeightBottom.value)
        base_pol += AllplanGeo.Point3D(el_build.LengthCenterWidth.value + el_build.LengthTransition.value, el_build.LengthBottomCut.value + (el_build.WidthBottom.value - el_build.LengthBottomCut.value * 2 - el_build.WidthCentralLittle.value) / 2, el_build.HeightBottom.value)
        base_pol += AllplanGeo.Point3D(el_build.LengthCenterWidth.value + el_build.LengthTransition.value + (el_build.WidthBottom.value - el_build.LengthBottomCut.value * 2 - el_build.WidthCentralLittle.value) / 2, (el_build.WidthBottom.value - el_build.LengthBottomCut.value * 2 - el_build.WidthCentralLittle.value) / 2, el_build.HeightBottom.value - el_build.HeightBottomCut.value)
        base_pol += AllplanGeo.Point3D(el_build.LengthCenterWidth.value + (el_build.WidthBottom.value - el_build.LengthBottomCut.value * 2 - el_build.WidthCentralLittle.value) / 2, 0, el_build.HeightBottom.value - el_build.HeightBottomCut.value)
        base_pol += AllplanGeo.Point3D(el_build.LengthCenterWidth.value,el_build.LengthBottomCut.value, el_build.HeightBottom.value)
        path = AllplanGeo.Polyline3D()
        path += AllplanGeo.Point3D(el_build.LengthCenterWidth.value,el_build.LengthBottomCut.value, el_build.HeightBottom.value)
        path += AllplanGeo.Point3D(el_build.LengthCenterWidth.value - 10 ,el_build.LengthBottomCut.value + 10, el_build.HeightBottom.value - 10)

        err, polyhedron = AllplanGeo.CreatePolyhedron(base_pol, path)

        
        if err:
            return []

        return polyhedron

    def lower_part_addiction_3_2(self, el_build):
        base_pol = AllplanGeo.Polygon3D()
        base_pol += AllplanGeo.Point3D(el_build.Length.value - el_build.LengthCenterWidth.value, el_build.WidthBottom.value, el_build.HeightBottom.value - el_build.HeightBottomCut.value)
        base_pol += AllplanGeo.Point3D(el_build.Length.value - el_build.LengthCenterWidth.value, el_build.WidthBottom.value - el_build.LengthBottomCut.value, el_build.HeightBottom.value)
        base_pol += AllplanGeo.Point3D(el_build.Length.value - el_build.LengthCenterWidth.value, el_build.LengthBottomCut.value, el_build.HeightBottom.value)
        base_pol += AllplanGeo.Point3D(el_build.Length.value - el_build.LengthCenterWidth.value, 0, el_build.HeightBottom.value - el_build.HeightBottomCut.value)
        base_pol += AllplanGeo.Point3D(el_build.Length.value - el_build.LengthCenterWidth.value, el_build.WidthBottom.value, el_build.HeightBottom.value - el_build.HeightBottomCut.value)
        path = AllplanGeo.Polyline3D()
        path += AllplanGeo.Point3D(el_build.Length.value - el_build.LengthCenterWidth.value, el_build.WidthBottom.value, el_build.HeightBottom.value - el_build.HeightBottomCut.value)
        path += AllplanGeo.Point3D(el_build.Length.value, el_build.WidthBottom.value, el_build.HeightBottom.value - el_build.HeightBottomCut.value)

        err, polyhedron = AllplanGeo.CreatePolyhedron(base_pol, path)

        
        if err:
            return []

        return polyhedron

    def lower_part_addiction_4_2(self, el_build):
        base_pol = AllplanGeo.Polygon3D()
        base_pol += AllplanGeo.Point3D(el_build.LengthCenterWidth.value, el_build.LengthBottomCut.value, el_build.HeightBottom.value)
        base_pol += AllplanGeo.Point3D(el_build.LengthCenterWidth.value, 0, el_build.HeightBottom.value - el_build.HeightBottomCut.value)
        base_pol += AllplanGeo.Point3D(el_build.LengthCenterWidth.value + (el_build.WidthBottom.value - el_build.LengthBottomCut.value * 2 - el_build.WidthCentralLittle.value) / 2, 0, el_build.HeightBottom.value - el_build.HeightBottomCut.value)
        base_pol += AllplanGeo.Point3D(el_build.LengthCenterWidth.value, el_build.LengthBottomCut.value, el_build.HeightBottom.value)     
        path = AllplanGeo.Polyline3D()
        path += AllplanGeo.Point3D(el_build.LengthCenterWidth.value, el_build.LengthBottomCut.value, el_build.HeightBottom.value)
        path += AllplanGeo.Point3D(el_build.LengthCenterWidth.value, el_build.LengthBottomCut.value + 10, el_build.HeightBottom.value)

        err, polyhedron = AllplanGeo.CreatePolyhedron(base_pol, path)

        if err:
            return []

        return polyhedron

    def lower_part_addiction_2_3(self, el_build):
        base_pol = AllplanGeo.Polygon3D()
        base_pol += AllplanGeo.Point3D(el_build.Length.value - el_build.LengthCenterWidth.value, el_build.WidthBottom.value - el_build.LengthBottomCut.value, el_build.HeightBottom.value)
        base_pol += AllplanGeo.Point3D(el_build.Length.value - el_build.LengthCenterWidth.value - el_build.LengthTransition.value, el_build.WidthBottom.value - el_build.LengthBottomCut.value - (el_build.WidthBottom.value - el_build.LengthBottomCut.value * 2 - el_build.WidthCentralLittle.value) / 2, el_build.HeightBottom.value)
        base_pol += AllplanGeo.Point3D(el_build.Length.value - el_build.LengthCenterWidth.value - el_build.LengthTransition.value - (el_build.WidthBottom.value - el_build.LengthBottomCut.value * 2 - el_build.WidthCentralLittle.value) / 2, el_build.WidthBottom.value - (el_build.WidthBottom.value - el_build.LengthBottomCut.value * 2 - el_build.WidthCentralLittle.value) / 2, el_build.HeightBottom.value - el_build.HeightBottomCut.value)
        base_pol += AllplanGeo.Point3D(el_build.Length.value - el_build.LengthCenterWidth.value - (el_build.WidthBottom.value - el_build.LengthBottomCut.value * 2 - el_build.WidthCentralLittle.value) / 2, el_build.WidthBottom.value, el_build.HeightBottom.value - el_build.HeightBottomCut.value)
        base_pol += AllplanGeo.Point3D(el_build.Length.value - el_build.LengthCenterWidth.value, el_build.WidthBottom.value - el_build.LengthBottomCut.value, el_build.HeightBottom.value)
        path = AllplanGeo.Polyline3D()
        path += AllplanGeo.Point3D(el_build.Length.value - el_build.LengthCenterWidth.value, el_build.WidthBottom.value - el_build.LengthBottomCut.value, el_build.HeightBottom.value)
        path += AllplanGeo.Point3D(el_build.Length.value - el_build.LengthCenterWidth.value + 10, el_build.WidthBottom.value - el_build.LengthBottomCut.value - 10, el_build.HeightBottom.value + 10)

        err, polyhedron = AllplanGeo.CreatePolyhedron(base_pol, path)
      
        if err:
            return []

        return polyhedron

    def lower_part_addiction_3_3(self, el_build):
        base_pol = AllplanGeo.Polygon3D()
        base_pol += AllplanGeo.Point3D(el_build.Length.value - el_build.LengthCenterWidth.value, el_build.WidthBottom.value - el_build.LengthBottomCut.value, el_build.HeightBottom.value)
        base_pol += AllplanGeo.Point3D(el_build.Length.value - el_build.LengthCenterWidth.value, el_build.WidthBottom.value, el_build.HeightBottom.value - el_build.HeightBottomCut.value)
        base_pol += AllplanGeo.Point3D(el_build.Length.value - el_build.LengthCenterWidth.value - (el_build.WidthBottom.value - el_build.LengthBottomCut.value * 2 - el_build.WidthCentralLittle.value) / 2, el_build.WidthBottom.value, el_build.HeightBottom.value - el_build.HeightBottomCut.value)
        base_pol += AllplanGeo.Point3D(el_build.Length.value - el_build.LengthCenterWidth.value, el_build.WidthBottom.value - el_build.LengthBottomCut.value, el_build.HeightBottom.value)
        path = AllplanGeo.Polyline3D()
        path += AllplanGeo.Point3D(el_build.Length.value - el_build.LengthCenterWidth.value, el_build.WidthBottom.value - el_build.LengthBottomCut.value, el_build.HeightBottom.value)
        path += AllplanGeo.Point3D(el_build.Length.value - el_build.LengthCenterWidth.value, el_build.WidthBottom.value - el_build.LengthBottomCut.value - 10, el_build.HeightBottom.value)

        err, polyhedron = AllplanGeo.CreatePolyhedron(base_pol, path)

        
        if err:
            return []

        return polyhedron

    def lower_part_addiction_2_4(self, el_build):
        base_pol = AllplanGeo.Polygon3D()
        base_pol += AllplanGeo.Point3D(el_build.Length.value - el_build.LengthCenterWidth.value, el_build.LengthBottomCut.value, el_build.HeightBottom.value)
        base_pol += AllplanGeo.Point3D(el_build.Length.value - el_build.LengthCenterWidth.value - el_build.LengthTransition.value, el_build.LengthBottomCut.value + (el_build.WidthBottom.value - el_build.LengthBottomCut.value * 2 - el_build.WidthCentralLittle.value) / 2, el_build.HeightBottom.value)
        base_pol += AllplanGeo.Point3D(el_build.Length.value - el_build.LengthCenterWidth.value - el_build.LengthTransition.value - (el_build.WidthBottom.value - el_build.LengthBottomCut.value * 2 - el_build.WidthCentralLittle.value) / 2, (el_build.WidthBottom.value - el_build.LengthBottomCut.value * 2 - el_build.WidthCentralLittle.value) / 2, el_build.HeightBottom.value - el_build.HeightBottomCut.value)
        base_pol += AllplanGeo.Point3D(el_build.Length.value - el_build.LengthCenterWidth.value - (el_build.WidthBottom.value - el_build.LengthBottomCut.value * 2 - el_build.WidthCentralLittle.value) / 2, 0, el_build.HeightBottom.value - el_build.HeightBottomCut.value)
        base_pol += AllplanGeo.Point3D(el_build.Length.value - el_build.LengthCenterWidth.value, el_build.LengthBottomCut.value, el_build.HeightBottom.value)
        path = AllplanGeo.Polyline3D()
        path += AllplanGeo.Point3D(el_build.Length.value - el_build.LengthCenterWidth.value, el_build.LengthBottomCut.value, el_build.HeightBottom.value)
        path += AllplanGeo.Point3D(el_build.Length.value - el_build.LengthCenterWidth.value - 10, el_build.LengthBottomCut.value + 10, el_build.HeightBottom.value - 10)

        err, polyhedron = AllplanGeo.CreatePolyhedron(base_pol, path)
       
        if err:
            return []

        return polyhedron

    def lower_part_addiction_3_4(self, el_build):
        base_pol = AllplanGeo.Polygon3D()
        base_pol += AllplanGeo.Point3D(el_build.Length.value - el_build.LengthCenterWidth.value, el_build.LengthBottomCut.value, el_build.HeightBottom.value)
        base_pol += AllplanGeo.Point3D(el_build.Length.value - el_build.LengthCenterWidth.value, 0, el_build.HeightBottom.value - el_build.HeightBottomCut.value)
        base_pol += AllplanGeo.Point3D(el_build.Length.value - el_build.LengthCenterWidth.value - (el_build.WidthBottom.value - el_build.LengthBottomCut.value * 2 - el_build.WidthCentralLittle.value) / 2, 0, el_build.HeightBottom.value - el_build.HeightBottomCut.value)
        base_pol += AllplanGeo.Point3D(el_build.Length.value - el_build.LengthCenterWidth.value, el_build.LengthBottomCut.value, el_build.HeightBottom.value)
        path = AllplanGeo.Polyline3D()
        path += AllplanGeo.Point3D(el_build.Length.value - el_build.LengthCenterWidth.value, el_build.LengthBottomCut.value, el_build.HeightBottom.value)
        path += AllplanGeo.Point3D(el_build.Length.value - el_build.LengthCenterWidth.value, el_build.LengthBottomCut.value + 10, el_build.HeightBottom.value)

        err, polyhedron = AllplanGeo.CreatePolyhedron(base_pol, path)
       
        if err:
            return []

        return polyhedron

    def last_lower_part(self, el_build):
        base_pol = AllplanGeo.Polygon3D()
        base_pol += AllplanGeo.Point3D(0, 20, 0)
        base_pol += AllplanGeo.Point3D(0, el_build.WidthBottom.value - 20, 0)
        base_pol += AllplanGeo.Point3D(0, el_build.WidthBottom.value, 20)
        base_pol += AllplanGeo.Point3D(0, el_build.WidthBottom.value, el_build.HeightBottom.value - el_build.HeightBottomCut.value)
        base_pol += AllplanGeo.Point3D(0, 0, el_build.HeightBottom.value - el_build.HeightBottomCut.value)
        base_pol += AllplanGeo.Point3D(0, 0, 20)
        base_pol += AllplanGeo.Point3D(0, 20, 0)
        if not GeometryValidate.is_valid(base_pol):
            return
        path = AllplanGeo.Polyline3D()
        path += AllplanGeo.Point3D(0, 20, 0)
        path += AllplanGeo.Point3D(el_build.Length.value,20,0)
        err, polyhedron = AllplanGeo.CreatePolyhedron(base_pol, path)     
        if err:
            return []

        return polyhedron


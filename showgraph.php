// generate the codecoverage graph

<?php // content="text/plain; charset=utf-8"
require_once ('../../../jpgraph/src/jpgraph.php');
require_once ('../../../jpgraph/src/jpgraph_bar.php');
require_once ('../../../jpgraph/src/jpgraph_line.php');

//bar1
$datay1=array();
//bar2
$datay2=array();
//bar3
$datay3=array();

$datax=array();
$months=array();
$q=$_GET["q"];
if(!$q)
{
	$q="/..";
}
$fn_total;
$fn_uncov;
$ChangeListId;
$fn_required;
$db = oci_connect('***', '****', '//localhost/****');
if (!$db) {
            echo( "<P>Unable to connect to the " .  "Hridyesh database server at this time.</P>" );
            exit();
            }
         			
	
$query="select unique ChangeListId,CREATE_DATE from codecoverage.A12_cl_cov order by CREATE_DATE";

$res = oci_parse($db,$query);
if (!$res) {
       echo("<P>Error performing query: " .
       mysql_error() . "</P>");
       exit();
 }
 oci_execute($res);
while ( $row = oci_fetch_array($res) ){
		$ChangeListId=$row['CHANGELISTID'];
		$query1="select * from codecoverage.A12_cl_cov where ChangeListId='".$ChangeListId."' and AssetPathId ='".$q."'"  ;
		
		$res1 = oci_parse($db,$query1);
		if (!$res) {
				echo("<P>Error performing query: " .
				mysql_error() . "</P>");
				exit();
		}
		oci_execute($res1);
		while ( $row1 = oci_fetch_array($res1) ){
		$version=$row1['VERSION'];
		$ChangeListId=$row1['CHANGELISTID']. "\n" ."($version)";
		$AssetPathId=$row1['ASSETPATHID'];
		$fn_uncov_per1=$row1['FN_UNCOV_PER'];
		$fn_uncov=$row1['FN_UNCOV'];
		$fn_required=$row1['FN_REQUIRED'];
		$fn_cov=$row1['FN_COV'];
		$fn_total=$row1['FN_TOTAL'];
		array_push($datay1,$fn_uncov_per1);
		array_push($datax,$ChangeListId);
		}		
								
	}

oci_close($db);
if (strcmp($q,"/..") ==0)
{
 $q="Overall";
}
$graph = new Graph(900,350);
$graph->SetScale("textlin");


$theme_class=new GreenTheme;

$graph->SetTheme($theme_class);

$graph->title->Set("Percentage Function Covered for $q");
$graph->SetBox(true);




$graph->xaxis->scale->SetGrace(50);
$graph->SetScale('textlin',15,85); 
//$graph->xaxis->SetLabelAngle(90);
$graph->yscale->SetAutoTicks();
$graph->yaxis->title->SetMargin(0);
$graph->title->SetColor('navy');
$graph->yaxis->title->SetFont(FF_ARIAL,FS_NORMAL,11);
$graph->yaxis->title->SetColor('navy');
$graph->yaxis->title->Set('Percentage Function Covered');
$graph->xaxis->title->SetColor('navy');
$graph->xaxis->title->SetMargin(70);
$graph->xaxis->title->SetFont(FF_ARIAL,FS_NORMAL,8);
$graph->xaxis->title->Set('ChangeList');

$graph->xaxis->SetLabelAngle(90);

$graph->yscale->SetAutoTicks(); 
$graph->yaxis->HideZeroLabel(true);
$graph->yaxis->HideLine(false);
$graph->yaxis->HideTicks(false,false);

$graph->xgrid->Show();
$graph->xgrid->SetLineStyle("solid");
$graph->xaxis->SetTickLabels($datax);
$graph->xgrid->SetColor('#E3E3E3');

// Create the first line
$p1 = new LinePlot($datay1);
$p1->SetColor('red');
$graph->Add($p1);
$p1->mark->SetType(MARK_IMG,'../Acrobat/images.jpeg',0.05);

$p1->value->SetFormat('%s');
$p1->value->Show();

$p1->SetColor("#6495ED");
$graph->legend->SetPos(0.5,0.995,'center','bottom');
$p1->SetLegend("Total Functions in $q=$fn_total ,Functions needed to reach 50%=$fn_required");



$graph->legend->SetFrameWeight(1);

// Output line
$graph->Stroke();

?>

//Part of Patch upload Automation tool 

import java.util.ArrayList;
import java.util.HashMap;

import java.util.Iterator;

import java.util.Map;

import java.util.Set;

import javax.el.ELContext;
import javax.el.ExpressionFactory;
import javax.el.ValueExpression;
import javax.faces.application.FacesMessage;
import javax.faces.component.UIComponent;
import javax.faces.context.ExternalContext;
import javax.faces.context.FacesContext;
import javax.faces.event.ActionEvent;
import javax.faces.event.ValueChangeEvent;
import javax.faces.validator.ValidatorException;
import oracle.adf.model.BindingContext;
import oracle.adf.model.binding.DCIteratorBinding;
import oracle.adf.view.rich.component.rich.data.RichTable;
import oracle.binding.BindingContainer;
import oracle.binding.OperationBinding;
import oracle.jbo.Row;
import oracle.jbo.ViewObject;
import javax.mail.*;


import javax.servlet.http.HttpServletRequest;

import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;

import model.AppModuleImpl;

import org.python.parser.ast.For;

import view.GetApprovalid;
import view.SendMail;
import view.UipTasks;

public class TagDB {
    private String url;
    public String userMail;
    private RichTable myTable;
    public String disable_button;
    public boolean disable_request_table=false;
    public boolean disable_approval_table=false;
    public boolean enable_series=true;
    public String mesg;
    public String labelid="";
    
    String result="";
    String label_name="";
    private RichTable request_form_table;

    public TagDB() {
        AppModuleImpl ami=new AppModuleImpl();
        userMail=ami.getUserPrincipalName();
        
    }
   
    public BindingContainer getBindings() {
      
        return BindingContext.getCurrent().getCurrentBindingsEntry();
    }

    


    public void setUrl(String url) {
        this.url = url;
    }

    public String getUrl() {
        return url;
    }

    public void setUserMail(String userMail) {
        this.userMail = userMail;
    }

    public String getUserMail() {
       
        return userMail;
    }

    public String delete() {
        BindingContainer bindings = getBindings();
        OperationBinding operationBinding = bindings.getOperationBinding("Delete");
        Object result = operationBinding.execute();
        if (!operationBinding.getErrors().isEmpty()) {
            return null;
        }
        OperationBinding operationBinding1 = bindings.getOperationBinding("Commit");
        Object result1 = operationBinding1.execute();
        if (!operationBinding1.getErrors().isEmpty()) {
            return null;
        }
        return null;
    }

    public void Verify_labelName(FacesContext facesContext,
                                 UIComponent uIComponent, Object object) {
        // Add event code here...
        label_name=(String) object;
        //System.out.println(">>label_name "+ label_name);
        String [] valid_label_name=label_name.split("_");
        int count=valid_label_name.length;
        if(count !=4) {
            FacesMessage message = new FacesMessage();
            message.setSummary(label_name +" is not in valid label format(PRODUCT_BRANCH_PLATFORM_DATE)");
            throw new ValidatorException(message);
        }
                    UipTasks status=new UipTasks();
                   
                    result= status.expiry_date(label_name);  
                    if((result.contains("not available"))|| (result.contains("No ADE volume defined"))) {
                        FacesMessage message = new FacesMessage();
                        message.setSummary(result);
                        throw new ValidatorException(message);
                    }
                    else
                    {
                    this.addMessage(FacesMessage.SEVERITY_INFO,result);
                    }
                
                      //status.check_dbpublish(label_name);
                  }

 
    public void setMyTable(RichTable myTable) {
        this.myTable = myTable;
    }

    public RichTable getMyTable() {
        return myTable;
    }

    public void Remove_Status_fileld(FacesContext facesContext,
                                     UIComponent uIComponent, Object object) {
        String status=(String)object;
        if(status.length()>0) {
            FacesMessage message = new FacesMessage();
            message.setSummary("Please make Status filed empty");
            throw new ValidatorException(message);
        }
        
    }

    public String cil1_action() {
        BindingContainer bindings = getBindings();
        OperationBinding operationBinding = bindings.getOperationBinding("Delete");
        Object result = operationBinding.execute();
        if (!operationBinding.getErrors().isEmpty()) {
            return null;
        }
        //OperationBinding operationBinding1 = bindings.getOperationBinding("Commit");
                //Object result1 = operationBinding1.execute();
                //if (!operationBinding1.getErrors().isEmpty()) {
                //    return null;
               // }
        return null;
    }

    public void setDisable_button(String disable_button) {
        this.disable_button = disable_button;
    }

    public String getDisable_button() {
        return disable_button;
    }

    public String show_list() {
        disable_request_table=true;
        disable_approval_table=false;
        BindingContainer bindings = getBindings();
        OperationBinding operationBinding = bindings.getOperationBinding("ExecuteWithParams2");
        Object result = operationBinding.execute();
        if (!operationBinding.getErrors().isEmpty()) {
            return null;
        }
        return null;
    }

    public void setDisable_request_table(boolean disable_request_table) {
        this.disable_request_table = disable_request_table;
    }

    public boolean isDisable_request_table() {
        return disable_request_table;
    }

    public void setDisable_approval_table(boolean disable_approval_table) {
        this.disable_approval_table = disable_approval_table;
    }

    public boolean isDisable_approval_table() {
        return disable_approval_table;
    }

    public String Show_approval_list() {
        disable_request_table=false;
        disable_approval_table=true;
        BindingContainer bindings = getBindings();
        OperationBinding operationBinding = bindings.getOperationBinding("ExecuteWithParams1");
        Object result = operationBinding.execute();
        if (!operationBinding.getErrors().isEmpty()) {
            return null;
        }
        return null;
    }


    


    public void setEnable_series(boolean enable_series) {
        this.enable_series = enable_series;
    }

    public boolean isEnable_series() {
        return enable_series;
    }

    

    public void Series_validator(FacesContext facesContext,
                                 UIComponent uIComponent, Object object) {
        // Add event code here...
        //System.out.println(">>:"+object.toString());
        /*
        int index=Integer.parseInt(object.toString());
        if(index==0) {
            FacesMessage message = new FacesMessage();
            message.setSummary("Please select at least one valid choice");
            throw new ValidatorException(message);
            //this.addMessage(FacesMessage.SEVERITY_INFO,"plese select drop down."); 
        }
    */
    }
    
    public void approval_validator(FacesContext facesContext,
                                 UIComponent uIComponent, Object object) {
        // Add event code here...
        System.out.println("inside approval_validator>>:"+object.toString());
        //int index=Integer.parseInt(object.toString());
        if(object.toString().equals(null)) {
            FacesMessage message = new FacesMessage();
            message.setSummary("Please select at least one valid choice");
            throw new ValidatorException(message);
            //this.addMessage(FacesMessage.SEVERITY_INFO,"plese select drop down."); 
        }
        
    }
    
    public void addMessage(FacesMessage.Severity type, String message) {
        FacesContext fctx = FacesContext.getCurrentInstance();
        FacesMessage fm = new FacesMessage(type, message, null);
        fctx.addMessage(null, fm);
    }
          
          public Object resolveValueExpression(String el) {      
                    FacesContext facesContext = FacesContext.getCurrentInstance();
                    ELContext elContext = facesContext.getELContext();
                    ExpressionFactory expressionFactory =  facesContext.getApplication().getExpressionFactory();        
                    ValueExpression valueExp = expressionFactory.createValueExpression(elContext,el,Object.class);
                    return valueExp.getValue(elContext);
                }
                
                public void setValueToEL(String el, Object val) {
                    FacesContext facesContext = FacesContext.getCurrentInstance();
                    ELContext elContext = facesContext.getELContext();
                    ExpressionFactory expressionFactory =   facesContext.getApplication().getExpressionFactory();
                    ValueExpression exp = expressionFactory.createValueExpression(elContext, el, Object.class);
                    exp.setValue(elContext, val);
                }
    /**
     * @return
     */
    public String call_method () {
      
        
        System.out.println(">>calling call_method ");
        return "continue";
    }
    

    
    public void selectOneChoice1_valueChangeListener(ValueChangeEvent valueChangeEvent) {
        // Add event code here...
        try{
            System.out.println("\n*************Start: "+valueChangeEvent.getNewValue());
           this.setValueToEL("#{row.bindings.Series.inputValue}", valueChangeEvent.getNewValue()); //Change to proper attribute name inside EL if Series is not the list column
           System.out.println("\n*************Attribute Value from List Binding: "+this.resolveValueExpression("#{row.bindings.Series.attributeValue}"));
           
        }
           catch (NullPointerException e)
           {
               //flag=true;
               //System.out.println("\n*************Start: "+valueChangeEvent.getOldValue());
               //FacesMessage message = new FacesMessage();
               //message.setSummary("You have not select any Series,Please Select Series");
               //throw new ValidatorException(message);
               
           }
    }

    public String cb1_action2() {
        enable_series=true;
        int flag=0;
        BindingContainer bindings = getBindings();
        DCIteratorBinding dciter =(DCIteratorBinding) bindings.get("ViewObj_emptyRequest1Iterator");
        ViewObject viewObjt =dciter.getViewObject();
        viewObjt .setRangeSize(-1);
        Row[] rows = viewObjt.getAllRowsInRange();
        GetApprovalid ids=new GetApprovalid();
        for (int i=0;i<rows.length;i++) {
            
            Row r = rows[i];
            String label_name;
            label_name = r.getAttribute("Label").toString();

            String Series_name  = r.getAttribute("Series").toString();
            System.out.println(">>:"+label_name+ " : "+Series_name);
        
            int result=ids.check_already_tagged_request(label_name, Series_name);
            if(result==0) {
                //FacesMessage message = new FacesMessage();
                //message.setSummary("Tag request for "+label_name+" to "+Series_name+" is already submitted for ");
                //throw new ValidatorException(message);
                this.addMessage(FacesMessage.SEVERITY_ERROR,"Tag request for "+label_name+" to "+Series_name+" is already submitted.");
                flag=1;
            }
        }
       if(flag==0)
       {
        OperationBinding operationBinding = bindings.getOperationBinding("MyCreateMethod");
        Object result = operationBinding.execute();
        if (!operationBinding.getErrors().isEmpty()) {
            return null;
        }
       }
        return null;
    }

    public String commit_new_request() {
       
        BindingContainer bindings = getBindings();
        
        OperationBinding operationBinding = bindings.getOperationBinding("Commit");
        Object result = operationBinding.execute();
        if (!operationBinding.getErrors().isEmpty()) {
            return null;
        }
      
       //HashMap group = new HashMap();
        GetApprovalid ids=new GetApprovalid();
        
       HashMap hm = new HashMap();
       String requester_name="";
        DCIteratorBinding dciter =(DCIteratorBinding) bindings.get("ViewObj_emptyRequest1Iterator");
                for (int i=0 ;i<dciter.getViewObject().getEstimatedRowCount() ;i++ ) {
                    String key="";
                    Row r=dciter.getRowAtRangeIndex(i);
                   
                     requester_name=r.getAttribute("RequesterId").toString();
                     String label_name=r.getAttribute("Label").toString();
                     String series_name=r.getAttribute("Series").toString();
                     String approval_id=r.getAttribute("ApprovalId").toString();
                    
                     System.out.println("\n>>"+requester_name);
                     System.out.println(":"+label_name);
                     System.out.println(":"+series_name);
                     System.out.println(":"+approval_id);
                    
                    String result_ids;
                     if(!approval_id.contains("@"))
                     {
                        result_ids=ids.Get_Mail_Ids(approval_id);
                     
                     }
                    else {
                         result_ids=approval_id;
                         System.out.println(":"+result_ids);
                     }
                    
                    String hash_value=series_name+"%"+result_ids;
                    boolean blnExists = hm.containsKey(label_name);
                    //ArrayList list = new ArrayList();
                    if(blnExists)
                    {
                            String pre_val=hm.get(label_name).toString();
                            hm.remove(label_name);
                            pre_val =pre_val+","+hash_value;
                            //list.add(pre_val);
                            hm.put(label_name,pre_val);
                            System.out.println("Making single request :"+label_name + " : " + pre_val );
                        }
                     else {
                        //list.add(hash_value);
                        hm.put(label_name,hash_value);
                        System.out.println("Making NEW request :"+label_name + " : " + hash_value );
                    }
                    
                   
                }
       
       
          
       //String message="";
       SendMail mail_notify=new SendMail();
       Set set1 = hm.entrySet();
       Iterator iii = set1.iterator();
               String req_reqid="";
       while(iii.hasNext()){
             Map.Entry me = (Map.Entry)iii.next();
             String label_request=me.getKey().toString();
            
             String label_values=me.getValue().toString();
           
             
             if(label_values.contains(",")) {
                 String [] series=label_values.split(",");
                 String message = "Hi All,<br><br>This is to inform there is a panding Tag Request and needs your attention.";
                  message+="<br><br>";
                  message+="<table border='1' cellpadding='0' cellspacing='0' width='600'>";
                  message+="<th>Label</th>";
                  message+="<th>Series</th>";
                  message+="<th>Request ID</th>";
                 for(int j=0;j<series.length;j++) {
                     System.out.println("**** 1"+label_request);
                         System.out.println("**** 1"+label_values);
                     String[] req=series[j].split("%");
                     String req_series=req[0];
                     req_reqid=req[1];
                     message+="<tr><td align='center' width='300'>"+label_request+"</td>";
                     message+="<td align='center'>"+req_series+"</td>";
                     message+="<td align='center'>"+requester_name+"</td>";
                    
                 }
                 message+="</tr>";
                 message+="</table>";
                 message+="<br>For more details, please visit the <a href='http://live.us.oracle.com/TagDB/faces/status?label="+label_request+'>'+"link</a> .<br><br>";
                 message+="Thanks.";
                 String subject="**Action Required: There is a pending Tag request for "+label_request;
                 try
                 {
                 mail_notify.postMail(req_reqid,subject,message,requester_name,requester_name);
                 }       catch(MessagingException e) {
           System.out.println("no able to send");
       }
             }
             
             else {
                     String message = "Hi All,<br><br>This is to inform there is a panding Tag Request and needs your attention.";
                      message+="<br><br>";
                      message+="<table border='1' cellpadding='0' cellspacing='0' width='600'>";
                      message+="<th>Label</th>";
                      message+="<th>Series</th>";
                      message+="<th>Request ID</th>";
                 //label_values.contains(",")
                 System.out.println("**** 2"+label_request);
                     System.out.println("**** 2"+label_values);
                 req_reqid="";
                 String[] req=label_values.split("%");
                 String req_series=req[0];
                 req_reqid=req[1];
                 message+="<tr><td align='center' width='300'>"+label_request+"</td>";
                 message+="<td align='center'>"+req_series+"</td>";
                 message+="<td align='center'>"+req_reqid+"</td>";
                  message+="</tr>";
                     message+="</table>";
                     message+="<br>For more details, please visit the <a href='http://live.us.oracle.com/TagDB/faces/status?label="+label_request+'>'+"link</a> .<br><br>";
                     message+="Thanks.";
                     String subject="**Action Required: There is a pending Tag request for "+label_request;
                     try
                     {
                     mail_notify.postMail(req_reqid,subject,message,requester_name,requester_name);
                     }
                     catch(MessagingException e) {
                         System.out.println("no able to send");
                     }
                 }
                 
             }
             //System.out.println("****"+me.getKey() + " : " + me.getValue() );
          
        DCIteratorBinding dciter1 = (DCIteratorBinding)bindings.get("ViewObj_emptyRequest1Iterator");
        dciter1.executeQuery();
        dciter1.refresh(DCIteratorBinding.RANGESIZE_UNLIMITED);
      
        return "commit";
   }
    
    public void create_mail() {
                   
    }
    public void setLabel_name(String label_name) {
        this.label_name = label_name;
    }

    public String getLabel_name() {
        return label_name;
    }

    public void setRequest_form_table(RichTable request_form_table) {
        this.request_form_table = request_form_table;
    }

    public RichTable getRequest_form_table() {
        return request_form_table;
    }


    public void edif_for_label_verify(FacesContext facesContext,
                                      UIComponent uIComponent, Object object) {
        // Add event code here...
        String new_label_name=(String) object;
        System.out.println(">>label_name "+ new_label_name);
    }

    public String cil2_action() {
        BindingContainer bindings = getBindings();
        OperationBinding operationBinding = bindings.getOperationBinding("Delete");
        Object result = operationBinding.execute();
        if (!operationBinding.getErrors().isEmpty()) {
            return null;
        }
        
        OperationBinding operationBinding1 = bindings.getOperationBinding("Commit");
        Object result1 = operationBinding1.execute();
        if (!operationBinding1.getErrors().isEmpty()) {
            return null;
        }
        return null;
    }
    
    
    public void doLogout(ActionEvent ae) {
        try {
            //System.out.println("Logout Invoked.");
            
            ExternalContext context = FacesContext.getCurrentInstance().getExternalContext();
            HttpServletResponse response = (HttpServletResponse) context.getResponse();
            HttpServletRequest request = (HttpServletRequest) context.getRequest();
            String url = request.getRequestURL().toString();
            
            //System.out.println(url);
           
            String direct = "http://www.oracle.com";
            //System.out.println(direct);
            response.setHeader( "Osso-Return-Url" , direct);
            HttpSession session = request.getSession();            
            if(session != null) {
                //System.out.println("Session is NOT NULL");
                session.invalidate();            
            }
            //System.out.println("Session is NULL and Logout.");
            response.sendError( 470, "Oracle SSO" );
        }catch(Exception e) {
            e.printStackTrace();
        }
    }

    public String create_new_tag_request() {
        BindingContainer bindings = getBindings();
        OperationBinding operationBinding = bindings.getOperationBinding("MyCreateMethod");
        Object result = operationBinding.execute();
        if (!operationBinding.getErrors().isEmpty()) {
            return null;
        }
       
        DCIteratorBinding dciter = (DCIteratorBinding)bindings.get("ViewObj_show_all_record_firstpage1Iterator");
        dciter.executeQuery();
        dciter.refresh(DCIteratorBinding.RANGESIZE_UNLIMITED);
        return "request";
    }

    public void setLabelid(String labelid) {
        this.labelid = labelid;
    }

    public String getLabelid() {
        return labelid;
    }
}



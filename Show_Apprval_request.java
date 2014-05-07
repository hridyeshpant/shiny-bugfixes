//Part of Patch upload Automation tool

import javax.faces.context.ExternalContext;
import javax.faces.context.FacesContext;

import javax.servlet.http.HttpServletRequest;

import oracle.adf.model.BindingContext;

import oracle.adf.model.binding.DCIteratorBinding;

import oracle.binding.BindingContainer;
import oracle.binding.OperationBinding;

public class Show_Apprval_request {
   public String  label_name_data;
    public Show_Apprval_request() {
        show_request();
    }

    public BindingContainer getBindings() {
        return BindingContext.getCurrent().getCurrentBindingsEntry();
    }

    public String show_request() {
        TagDB data=new TagDB();
        ExternalContext context = FacesContext.getCurrentInstance().getExternalContext();
        HttpServletRequest request = (HttpServletRequest) context.getRequest();
        
        String remoteUserDn = request.getHeader("Osso-User-Dn");
        String label_name = request.getParameter("label");
        label_name_data=label_name;
        
        BindingContainer bindings = getBindings();
        //System.out.print("calling cb2_action2 with "+data.userMail+" : "+label_name);
        OperationBinding operationBinding = bindings.getOperationBinding("MyApproveMethod1");
        operationBinding.getParamsMap().put("user", data.userMail);
        operationBinding.getParamsMap().put("label", label_name);
        Object result = operationBinding.execute();
        if (!operationBinding.getErrors().isEmpty()) {
            return null;
        }
        return null;
        
    }


    public void setLabel_name_data(String label_name_data) {
        this.label_name_data = label_name_data;
    }

    public String getLabel_name_data() {
        return label_name_data;
    }

    public String cb1_action() {
        BindingContainer bindings = getBindings();
        OperationBinding operationBinding = bindings.getOperationBinding("Commit");
        Object result = operationBinding.execute();
        if (!operationBinding.getErrors().isEmpty()) {
            return null;
        }
        show_request();
        //DCIteratorBinding dciter1 = (DCIteratorBinding)bindings.get("ViewObj_showlist_based_on_id1Iterator");
        //dciter1.executeQuery();
        //dciter1.refresh(DCIteratorBinding.RANGESIZE_UNLIMITED);
        
        return "return_home";
    }
}

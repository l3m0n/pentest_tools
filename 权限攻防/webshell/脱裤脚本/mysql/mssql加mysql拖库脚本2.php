<%@ Page Language="C#" %>
 
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
 
<script runat="server">
    protected void Page_Load(object sender, EventArgs e)
    {
        //if (Request["sub"] != null && Request["sub"] == "submit")
        //{
        //    GridView1.Visible = true;
 
        //    //System.Web.HttpContext.Current.Response.Write(DropDownList1.SelectedIndex);
        //    if (DropDownList1.SelectedIndex == 0)
        //    {
        //        using (System.Data.Odbc.OdbcConnection conn = new System.Data.Odbc.OdbcConnection(Request["conn"]))
        //        {
        //            conn.Open();
        //            System.Data.Odbc.OdbcCommand comm = new System.Data.Odbc.OdbcCommand(Request["sql"], conn);
        //            System.Data.Odbc.OdbcDataAdapter ad = new System.Data.Odbc.OdbcDataAdapter();
        //            ad.SelectCommand = comm;
        //            System.Data.DataSet ds = new System.Data.DataSet();
        //            ad.Fill(ds);
        //            GridView1.DataSource = ds;
        //            GridView1.DataBind();
        //        }
        //    }
        //    if (DropDownList1.SelectedIndex == 2)
        //    {
        //        using (System.Data.SqlClient.SqlConnection conn = new System.Data.SqlClient.SqlConnection(Request["conn"]))
        //        {
        //            conn.Open();
        //            System.Data.SqlClient.SqlCommand comm = new System.Data.SqlClient.SqlCommand(Request["sql"], conn);
        //            System.Data.SqlClient.SqlDataAdapter ad = new System.Data.SqlClient.SqlDataAdapter();
        //            ad.SelectCommand = comm;
        //            System.Data.DataSet ds = new System.Data.DataSet();
        //            ad.Fill(ds);
        //            GridView1.DataSource = ds;
        //            GridView1.DataBind();
        //        }
 
        //    }
        //    if (DropDownList1.SelectedIndex == 1)
        //    {
        //        using (System.Data.OleDb.OleDbConnection conn = new System.Data.OleDb.OleDbConnection(Request["conn"]))
        //        {
        //            conn.Open();
        //            System.Data.OleDb.OleDbCommand comm = new System.Data.OleDb.OleDbCommand(Request["sql"], conn);
        //            System.Data.OleDb.OleDbDataAdapter ad = new System.Data.OleDb.OleDbDataAdapter();
        //            ad.SelectCommand = comm;
        //            System.Data.DataSet ds = new System.Data.DataSet();
        //            ad.Fill(ds);
        //            GridView1.DataSource = ds;
        //            GridView1.DataBind();
        //        }
        //    }
        //}
 
    }
 
 
 
protected void  DropDownList1_SelectedIndexChanged(object sender, EventArgs e)
{
    connT.Text = DropDownList1.SelectedValue.ToString();
    GridView1.Visible = false;
    DropDownList2.Items.Clear();
}
 
protected void Button1_Click(object sender, EventArgs e)
 
{
    if (DropDownList1.SelectedIndex == 0)
    {
        using (System.Data.Odbc.OdbcConnection conn = new System.Data.Odbc.OdbcConnection(connT.Text.ToString()))
        //using (System.Data.OleDb.OleDbConnection conn = new System.Data.OleDb.OleDbConnection(connT.Text.ToString()))
        {
            conn.Open();
            System.Data.DataTable dt = conn.GetSchema("Tables");
 
            //GridView1.DataSource = dt;
            //GridView1.DataBind();
            //GridView1.Visible = true;
            //DropDownList2.DataSource = dt.Select("TABLE_TYPE='TABLE'");
            //DropDownList2.DataValueField = "TABLE_NAME";
            //DropDownList2.DataTextField = "TABLE_NAME";
            //DropDownList2.DataBind();
            DropDownList2.Items.Clear();
            foreach (System.Data.DataRow item in dt.Select("TABLE_TYPE='TABLE'"))
            {
 
                DropDownList2.Items.Add(new ListItem(item["TABLE_NAME"].ToString(), item["TABLE_NAME"].ToString()));
 
            }
        }
    }
    if (DropDownList1.SelectedIndex == 1)
    {
        using (System.Data.OleDb.OleDbConnection conn = new System.Data.OleDb.OleDbConnection(connT.Text.ToString()))
        {
            conn.Open();
            System.Data.DataTable dt = conn.GetSchema("Tables");
 
            //GridView1.DataSource = dt;
            //GridView1.DataBind();
            //GridView1.Visible = true;
            //DropDownList2.DataSource = dt.Select("TABLE_TYPE='TABLE'");
            //DropDownList2.DataValueField = "TABLE_NAME";
            //DropDownList2.DataTextField = "TABLE_NAME";
            //DropDownList2.DataBind();
            DropDownList2.Items.Clear();
            foreach (System.Data.DataRow item in dt.Select("TABLE_TYPE='TABLE'"))
            {
 
                DropDownList2.Items.Add(new ListItem(item["TABLE_NAME"].ToString(), item["TABLE_NAME"].ToString()));
 
            }
        }
    }
    if (DropDownList1.SelectedIndex == 2)
    {
        using (System.Data.SqlClient.SqlConnection conn = new System.Data.SqlClient.SqlConnection(connT.Text.ToString()))
                {
            conn.Open();
            System.Data.SqlClient.SqlCommand comm = new System.Data.SqlClient.SqlCommand("select name from sysobjects where type='U'", conn);
            //System.Data.SqlClient.SqlDataReader dr = comm.ExecuteReader();
            //string UserTable = "";
            //while (dr.Read())
            //{
            //    UserTable = (string)dr[0];
            //    DropDownList2.Items.Add(UserTable); 
 
            //}
            System.Data.SqlClient.SqlDataAdapter ad = new System.Data.SqlClient.SqlDataAdapter();
            ad.SelectCommand = comm;
            System.Data.DataSet ds = new System.Data.DataSet();
            ad.Fill(ds);
 
            DropDownList2.DataSource = ds;
 
            DropDownList2.DataTextField = "name";
            DropDownList2.DataValueField = "name";
            DropDownList2.DataBind();
 
 
        }
    }
}
 
protected void Button2_Click(object sender, EventArgs e)
{
    string provoder = "";
 
 
    if (DropDownList1.SelectedIndex == 1)
        provoder = "System.Data.OleDb";
    else if (DropDownList1.SelectedIndex == 2)
 
        provoder = "System.Data.SqlClient";
    else if (DropDownList1.SelectedIndex ==0)
    {
        provoder = "System.Data.Odbc";
    }
 
    System.Data.Common.DbProviderFactory factory = System.Data.Common.DbProviderFactories.GetFactory(provoder);
    System.Data.Common.DbConnection conn=factory.CreateConnection() ;
    conn.ConnectionString = connT.Text;
    conn.Open();
    System.Data.Common.DbCommand comm = conn.CreateCommand();
    comm.CommandText = Request["sql"];
    System.Data.Common.DbDataReader dr= comm.ExecuteReader();
    GridView1.DataSource = dr;
    GridView1.DataBind();
    GridView1.Visible = true;
    dr.Close();
    comm.Dispose();
    conn.Close();
 
}
</script>
 
<html xmlns="http://www.w3.org/1999/xhtml">
<head runat="server">
    <title></title>
 
    <script language="javascript" type="text/javascript">
// <!CDATA[
 
        function Select1_onclick() {
            document.getElementById('conn').value = "dsn";
        }
 
// ]]>
    </script>
    <style type="text/css">
        #sql
        {
            width: 677px;
            height: 106px;
        }
    </style>
</head>
<body>
    <form id="form1" runat="server">
    <div>
        <table><tr><td >
    type:</td><td colspan="2"><asp:DropDownList ID="DropDownList1" runat="server" 
            onselectedindexchanged="DropDownList1_SelectedIndexChanged" 
            AutoPostBack="True">
            <asp:ListItem Value="dsn=;uid=;pwd=;">dsn</asp:ListItem>
            <asp:ListItem Value="Provider=Microsoft.Jet.OLEDB.4.0;Data Source=E:\database.mdb">access</asp:ListItem>
            <asp:ListItem Value="server=localhost;UID=sa;PWD=;database=master">mssql</asp:ListItem>
        </asp:DropDownList>
        <br/></td>
        </tr>
 
        <tr><td>
        conn: </td><td><asp:TextBox ID="connT" name="conn" runat="server" Width="680px"></asp:TextBox></td><td>
            <asp:Button 
                        ID="Button1" runat="server" Text="Go" 
                onclick="Button1_Click" />
                    <br/>
        </td></tr>
        <tr><td>tables</td><td colspan="2">
            <asp:DropDownList ID="DropDownList2"  runat="server">
            </asp:DropDownList>
        </td></tr>
        <tr><td>sqlstr:  </td><td><input type="text" name="sql" id="sql"  value="<% =Request["sql"]%>"/></td><td>
 
 
     <br />
            <asp:Button ID="Button2" runat="server" onclick="Button2_Click" Text="Exec" />
            </td></tr>
        </table>
        <asp:GridView ID="GridView1" runat="server" CellPadding="4" ForeColor="#333333" 
            GridLines="None">
            <RowStyle BackColor="#EFF3FB" />
            <FooterStyle BackColor="#507CD1" Font-Bold="True" ForeColor="White" />
            <PagerStyle BackColor="#2461BF" ForeColor="White" HorizontalAlign="Center" />
            <SelectedRowStyle BackColor="#D1DDF1" Font-Bold="True" ForeColor="#333333" />
            <HeaderStyle BackColor="#507CD1" Font-Bold="True" ForeColor="White" />
            <EditRowStyle BackColor="#2461BF" />
            <AlternatingRowStyle BackColor="White" />
        </asp:GridView>
    </div>
    </form>
</body>
</html>

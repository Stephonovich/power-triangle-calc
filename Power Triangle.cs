using System;
using System.Collections;
using System.Collections.Generic;
using System.Collections.Specialized;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;



namespace Power_Triangle
{
    public partial class Form1 : Form
    {
        double kw = 0;
        double kvar = 0;
        double kva = 0;
        double pf = 0;
        double theta = 0;

        public Form1()
        {
            InitializeComponent();
        }



        private void textBox5_TextChanged(object sender, EventArgs e)
        {

        }


        private void textBox4_TextChanged(object sender, EventArgs e)
        {

        }



        private void textBox3_TextChanged(object sender, EventArgs e)
        {

        }



        private void textBox2_TextChanged(object sender, EventArgs e)
        {

        }



        private void textBox1_TextChanged(object sender, EventArgs e)
        {

        }



        private void button1_Click(object sender, EventArgs e)
        {
            Dispatch();
        }



        private void button3_Click(object sender, EventArgs e)
        {
            Close();
        }



        private void button2_Click(object sender, EventArgs e)
        {
            ResetForm();
        }



        private void ResetForm()
        {
            foreach (var c in this.Controls)
            {
                if (c is TextBox)
                {
                    ((TextBox)c).Text = String.Empty;
                }
            }
        }



        private Dictionary<string, double> GetInput()
        {
            // Make dict with text containing input, label relevant portion of form label
            // Keys are the labels on the form, with extraneous info removed
            // Values are the raw contents of the text boxes, null or otherwise

            var label_var = new Dictionary<string, string>();
            // Split twice to extract title, trim as there is leading and trailing whitespace
            string local_label_1 = label1.ToString().Split('(')[0].Split(':')[1].Trim();
            string local_label_2 = label2.ToString().Split('(')[0].Split(':')[1].Trim();
            string local_label_3 = label3.ToString().Split('(')[0].Split(':')[1].Trim();
            string local_label_4 = label4.ToString().Split('(')[0].Split(':')[1].Trim();
            string local_label_5 = label5.ToString().Split('(')[0].Split(':')[1].Trim();
            label_var[local_label_1] = textBox1.Text;
            label_var[local_label_2] = textBox2.Text;
            label_var[local_label_3] = textBox3.Text;
            label_var[local_label_4] = textBox4.Text;
            label_var[local_label_5] = textBox5.Text;


            // Make dict to hold only the non-null values
            var calc_vars = new Dictionary<string, double>();

            // Try to convert all values to doubles, giving them names used later
            // They're in a try block so the blanks can get caught
            // In the catch block, the foreach puts the two non-nulls into calc_vars dict
            try
            {
                kw = Convert.ToDouble(label_var[local_label_1]);
                kva = Convert.ToDouble(label_var[local_label_2]);
                kvar = Convert.ToDouble(label_var[local_label_3]);
                pf = Convert.ToDouble(label_var[local_label_4]);
                theta = Convert.ToDouble(label_var[local_label_5]);
            }

            catch (FormatException)
            {
                foreach (var pair in label_var)
                {
                    if (!String.IsNullOrEmpty(pair.Value))
                    {
                        calc_vars.Add(pair.Key, Convert.ToDouble(pair.Value));
                    }
                }
            }
            return calc_vars;
        }



        private void Dispatch()
        {
            // dispatch_input == calc_vars, which is a Dictionary (string/double)
            var dispatch_input = GetInput();
            var dispatch_list = new List<string>();

            foreach (var dispatch_var in dispatch_input)
            {
                dispatch_list.Add(dispatch_var.Key);
            }

            string dispatch_key = String.Join("_", dispatch_list.ToArray());

            switch(dispatch_key)
            {
                case "kW_kVA":
                    FromKwKva(dispatch_input["kW"], dispatch_input["kVA"]);
                    break;
                case "kW_kVAR":
                    FromKwKvar(dispatch_input["kW"], dispatch_input["kVAR"]);
                    break;
                case "kW_PF":
                    FromKwPf(dispatch_input["kW"], dispatch_input["PF"]);
                    break;
                case "kW_Theta":
                    FromKwTheta(dispatch_input["kW"], dispatch_input["Theta"]);
                    break;
                case "kVA_kVAR":
                    FromKvaKvar(dispatch_input["kVA"], dispatch_input["kVAR"]);
                    break;
                case "kVA_PF":
                    FromKvaPf(dispatch_input["kVA"], dispatch_input["PF"]);
                    break;
                case "kVA_Theta":
                    FromKvaTheta(dispatch_input["kVA"], dispatch_input["Theta"]);
                    break;
                case "kVAR_PF":
                    FromKvarPf(dispatch_input["kVAR"], dispatch_input["PF"]);
                    break;
                case "kVAR_Theta":
                    FromKvarTheta(dispatch_input["kVAR"], dispatch_input["Theta"]);
                    break;
                case "PF_Theta":
                    CatchInput();
                    break;
                default:
                    MessageBox.Show("Error");
                    break;
            }
        }

        /*
        private Dictionary<string, Action<string>> dispatch_dict =
            new Dictionary<string, Action<string>>
            {

                { "kW_kVA" , FromKwKva },
                { "kVA_kW" , "FromKwKva" },
                { "kW_kVAR" , "FromKwKvar" },
                { "kVAR_kW" , "FromKwKvar" },
                { "kW_PF" , "FromKwPf" },
                { "PF_kW" , "FromKwPf" },
                { "kW_Theta" , "FromKwTheta" },
                { "Theta_kW" , "FromKwTheta" },
                { "kVA_kVAR" , "FromKvaKvar" },
                { "kVAR_kVA" , "FromKvaKvar" },
                { "kVA_PF" , "FromKvaPf" },
                { "PF_kVA" , "FromKvaPf" },
                { "kVA_Theta" , "FromKvaTheta" },
                { "Theta_kVA" , "FromKvaTheta" },
                { "kVAR_PF" , "FromKvarPf" },
                { "PF_kVAR" , "FromKvarPf" },
                { "kVAR_Theta" , "FromKvarTheta" },
                { "Theta_kVAR" , "FromKvarTheta" },
                { "PF_Theta" , "CatchInput" },
                { "Theta_PF" , "CatchInput" }

            };
            */


        private double RadianToDegree(double angle_in_radians)
        {
            return angle_in_radians * (180 / Math.PI);
        }



        private double DegreeToRadian(double angle_in_degrees)
        {
            return angle_in_degrees * (Math.PI / 180);
        }



        private void FromKwKva(double kw, double kva)
        {
            theta = Math.Acos(kw / kva);
            kvar = Math.Sin(theta) * kva;
            pf = Math.Cos(theta);
            ReturnResults(kw, kvar, kva, pf, theta);
        }



        private void FromKwKvar(double kw, double kvar)
        {
            theta = Math.Atan(kvar / kw);
            pf = Math.Cos(theta);
            kva = kw / pf;
            ReturnResults(kw, kvar, kva, pf, theta);
        }



        private void FromKwPf(double kw, double pf)
        {
            theta = Math.Acos(pf);
            kvar = Math.Tan(theta) * kw;
            kva = kw / pf;
            ReturnResults(kw, kvar, kva, pf, theta);
        }



        private void FromKwTheta(double kw, double theta)
        {
            theta = DegreeToRadian(theta);
            kvar = Math.Tan(theta) * kw;
            pf = Math.Cos(theta);
            kva = kw / pf;
            ReturnResults(kw, kvar, kva, pf, theta);
        }



        private void FromKvaKvar(double kva, double kvar)
        {
            theta = Math.Asin(kvar / kva);
            pf = Math.Cos(theta);
            kw = kva * pf;
            ReturnResults(kw, kvar, kva, pf, theta);

        }



        private void FromKvaPf(double kva, double pf)
        {
            theta = Math.Acos(pf);
            kw = kva * pf;
            kvar = Math.Tan(theta) * kw;
            ReturnResults(kw, kvar, kva, pf, theta);

        }



        private void FromKvaTheta(double kva, double theta)
        {
            theta = DegreeToRadian(theta);
            pf = Math.Cos(theta);
            kw = kva * pf;
            kvar = Math.Tan(theta) * kw;
            ReturnResults(kw, kvar, kva, pf, theta);
        }



        private void FromKvarPf(double kvar, double pf)
        {
            theta = Math.Acos(pf);
            kva = kvar / Math.Sin(theta);
            kw = kva * pf;
            ReturnResults(kw, kvar, kva, pf, theta);
        }



        private void FromKvarTheta(double kvar, double theta)
        {
            theta = DegreeToRadian(theta);
            pf = Math.Cos(theta);
            kva = kvar / Math.Sin(theta);
            kw = kva * pf;
            ReturnResults(kw, kvar, kva, pf, theta);
        }
        


        private void CatchInput()
        {
            MessageBox.Show("Power Factor is cos(theta).\nPlease use other values.", "Inadequate Data");
        }



        private void ReturnResults(double kw, double kvar, double kva, double pf, double theta)
        {
            theta = RadianToDegree(theta); // Everything is done internally in radians

            string kw_disp = Convert.ToString(Math.Round(kw, 3));
            string kva_disp = Convert.ToString(Math.Round(kva, 3));
            string kvar_disp = Convert.ToString(Math.Round(kvar, 3));
            string pf_disp = Convert.ToString(Math.Round(pf, 3));
            string theta_disp = Convert.ToString(Math.Round(theta, 3));

            // This foreach will hit the non-text boxes, but they are ignored
            foreach (Control text_box_edit in this.Controls)
            {
                switch (text_box_edit.Name)
                {
                    case "textBox1":
                        text_box_edit.Text = kw_disp;
                        break;
                    case "textBox2":
                        text_box_edit.Text = kva_disp;
                        break;
                    case "textBox3":
                        text_box_edit.Text = kvar_disp;
                        break;
                    case "textBox4":
                        text_box_edit.Text = pf_disp;
                        break;
                    case "textBox5":
                        text_box_edit.Text = theta_disp;
                        break;
                }
            }
        }
    }
}

// Allows ToDegrees attribute extension to function in 3.0 framework.
namespace System.Runtime.CompilerServices
{
    class ExtensionAttribute : Attribute
    {

    }
}

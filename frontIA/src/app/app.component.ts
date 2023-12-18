import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';
import {FormsModule, NgForm} from '@angular/forms';
import { ApiService } from './ApiService/api-service.service';
import { HttpClientModule } from '@angular/common/http';
@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterOutlet, FormsModule, HttpClientModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent implements OnInit{
  title = 'frontIA';

  ngOnInit(): void {}
  formData: any = {};
  response: any;
  responseString: string= "";
  erro:string = "";
  constructor(private apiService: ApiService){}
  onSubmit(mainForm: NgForm){
    Object.keys(mainForm.controls).forEach(key => {
      this.formData[key] = mainForm.controls[key].value;
      const control = mainForm.controls[key];
      if (control.hasError('required') && !control.value) {
        this.erro = "É nessário preencher todos os campos"
        return; // Se um campo não estiver preenchido, não é necessário verificar os outros
      }

      try{
        const num=parseFloat(control.value)
        if (isNaN(num)) {
          throw new Error("Não é um número válido");
        }
      }catch(erro){
        this.erro = "Erro: Por favor, insira um número válido";
        return;
      }

    });

    for (const key in this.formData) {
      if (this.formData.hasOwnProperty(key)) {
        const value = this.formData[key];

        if (typeof value === 'number' && value < 0) {
          console.error('Erro: valor negativo encontrado!');
          this.erro = "Erro: valores negativos não permitidos"
          return;
        }
      }
    }

    const formJSON = JSON.stringify(this.formData);
    this.apiService.sendData(formJSON).subscribe(
      (data)=>{
        this.response = data;
        this.responseString = this.response ? "A água é potável": "A água não é potável"
        console.log(this.response)
      }
      )
  }
}

const tabs=[...document.querySelectorAll(".tab")], pages=[...document.querySelectorAll(".page")];
function showPage(id){pages.forEach(p=>p.classList.toggle("active",p.id===id));tabs.forEach(t=>t.classList.toggle("active",t.dataset.tab===id));}
function route(){const id=location.hash.replace("#","")||"home";showPage(pages.some(p=>p.id===id)?id:"home");}
window.addEventListener("hashchange",route);route();
const form=document.querySelector("#predict-form");
form.addEventListener("submit",async e=>{
 e.preventDefault();const data=Object.fromEntries(new FormData(form).entries());
 data.expected_students=Number(data.expected_students);data.portions_prepared=Number(data.portions_prepared);
 data.is_holiday=Number(data.is_holiday);data.exam_period=Number(data.exam_period);
 data.is_weekend=["Saturday","Sunday"].includes(data.day_of_week)?1:0;
 const btn=form.querySelector("button");btn.disabled=true;btn.textContent="Calculating forecast…";
 document.querySelector("#error").classList.add("hidden");
 try{
  const response=await fetch("/api/predict",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(data)});
  const result=await response.json();if(!response.ok)throw new Error(result.error||"The prediction service returned an error.");
  document.querySelector("#empty-state").classList.add("hidden");document.querySelector("#results").classList.remove("hidden");
  document.querySelector("#demand-result").textContent=result.predicted_demand.toLocaleString();
  document.querySelector("#prep-result").textContent=result.suggested_preparation.toLocaleString();
  document.querySelector("#waste-result").textContent=result.estimated_waste.toLocaleString();
  document.querySelector("#result-subtitle").textContent=data.meal_type+" · "+data.day_of_week;
  const diff=result.difference;
  document.querySelector("#advice").textContent=diff>0?`Your plan is ${diff} portions above estimated demand. Consider reviewing the planned quantity.`:"Your plan is at or below estimated demand. Maintain an appropriate service buffer.";
 }catch(err){const el=document.querySelector("#error");el.textContent=err.message;el.classList.remove("hidden");}
 finally{btn.disabled=false;btn.innerHTML='Run meal forecast <span>↗</span>';}
});

//https://qna.habr.com/q/587383 thanks

$(function() {

  $('input[type="checkbox"]').change(checkboxChanged);

  function checkboxChanged() {
    var $this = $(this),
        checked = $this.prop("checked"),
        container = $this.parent(),
        siblings = container.siblings();

    container.find('input[type="checkbox"]')
    .prop({
        indeterminate: false,
        checked: checked
    })
    .siblings('label')
    .removeClass('custom-checked custom-unchecked custom-indeterminate')
    .addClass(checked ? 'custom-checked' : 'custom-unchecked');

    checkSiblings(container, checked);
  }

  function checkSiblings($el, checked) {
    var parent = $el.parent().parent(),
        all = true,
        indeterminate = false;

    $el.siblings().each(function() {
      return all = ($(this).children('input[type="checkbox"]').prop("checked") === checked);
    });

    if (all && checked) {
      parent.children('input[type="checkbox"]')
      .prop({
          indeterminate: false,
          checked: checked
      })
      .siblings('label')
      .removeClass('custom-checked custom-unchecked custom-indeterminate')
      .addClass(checked ? 'custom-checked' : 'custom-unchecked');

      checkSiblings(parent, checked);
    } 
    else if (all && !checked) {
      indeterminate = parent.find('input[type="checkbox"]:checked').length > 0;

      parent.children('input[type="checkbox"]')
      .prop("checked", checked)
      .prop("indeterminate", indeterminate)
      .siblings('label')
      .removeClass('custom-checked custom-unchecked custom-indeterminate')
      .addClass(indeterminate ? 'custom-indeterminate' : (checked ? 'custom-checked' : 'custom-unchecked'));

      checkSiblings(parent, checked);
    } 
    else {
      $el.parents("li").children('input[type="checkbox"]')
      .prop({
          indeterminate: true,
          checked: false
      })
      .siblings('label')
      .removeClass('custom-checked custom-unchecked custom-indeterminate')
      .addClass('custom-indeterminate');
    }
  }
});
function getEventTarget(e) {
  e = e || window.event;
  return e.target || e.srcElement; 
  }

  var ul = document.getElementById('listofdistricts');
  ul.onclick = function(event) {
  var target = getEventTarget(event);
  let elemID = target.innerText;
  let cleanID = elemID.substring(0, elemID.length - 19);
  let element = document.getElementById(cleanID);
  //alert(cleanID)
  if (element){
  let hidden = element.getAttribute("hidden");

  if (hidden) {
  element.removeAttribute("hidden");
  } else {
  element.setAttribute("hidden", "hidden");
  }
  //alert(target.innerText);
  }
};
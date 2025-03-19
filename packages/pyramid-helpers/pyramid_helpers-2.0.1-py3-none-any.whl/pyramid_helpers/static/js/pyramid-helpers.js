/*
 * pyramid-helpers -- Helpers to develop Pyramid applications
 * By: Cyril Lacoux <clacoux@easter-eggs.com>
 *     Valéry Febvre <vfebvre@easter-eggs.com>
 *
 * Copyright (C) Cyril Lacoux, Easter-eggs
 * https://gitlab.com/yack/pyramid-helpers
 *
 * This file is part of pyramid-helpers.
 *
 * pyramid-helpers is free software; you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 *
 * pyramid-helpers is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

/* eslint no-console: "off" */

/*
 * Add `.createElementFromString()` method to document
 * Create a new dom element from raw html
 */
document.createElementFromString = function (html) {
    let div = document.createElement('div');

    div.innerHTML = html;

    return div.firstElementChild;
};


/*
 * Get first scrollable ancestor
 */
function getScrollable(element) {
    if (element === null) {
        return null;
    }

    if (element.scrollHeight > element.clientHeight) {
        return element;
    }

    return getScrollable(element.parentNode);
}


/*
 * Get a style property value
 */
function getStylePropertyValue(element, property, ispx=false) {
    let value = window.getComputedStyle(element, null).getPropertyValue(property);

    if (!value || !ispx) {
        return value;
    }

    return value.slice(0, -2);
}


/*
 * Transform a string to camel case
 */
function toCamelCase(str) {
    return str.toLowerCase().replace(/[^a-zA-Z0-9]+(.)/g, (m, chr) => chr.toUpperCase());
}


/*
 * I18n
 */
function translate(string) {
    return string;
}


/*
 * API error callback
 */
async function apiErrorCallback(response) {
    if (response.status >= 500) {
        notify.error(translate('Failed to communicate with remote server'));
        return;
    }

    const isJson = response.headers.get('content-type')?.includes('application/json');
    const data = isJson ? await response.json() : null;
    if (data?.message) {
        notify.error(data.message);
        return;
    }

    if (response.status == 403) {
        notify.error(translate('Access denied'));
    }
    else {
        notify.error(translate('An unexplained error occurred'));
    }
}


/*
 * API form setup
 */
function clearFormErrors(form) {
    form.querySelectorAll('.form-error').forEach(element => { element.remove(); });
}


function setFormErrors(form, errors) {
    let field;
    let message;
    let parts;
    let position;
    let values;

    for (let key in errors) {
        message = errors[key];

        field = form.querySelector('[name="' + key + '"]');
        if (!field) {
            // Field is multiple - field data type is NumberList, StringList or ForEach
            parts = key.split('-');
            if (parts.length != 2) {
                continue;
            }

            field = form.querySelector('[name="' + parts[0] + '"]');
            if (!field) {
                continue;
            }

            position = parseInt(parts.pop(1));

            if (!isNaN(position)) {
                values = field.value.split(',');
                message = values[position] + ': ' + message;
            }
        }

        field.after(document.createElementFromString(templates.formError({message: message})));
    }
}


/*
 * Partial block setup
 */
function partialBlockSetup(context) {
    if (!context) {
        context = document;
    }

    context.querySelectorAll('a.partial-link').forEach(element => {
        element.onclick = function(e) {
            e.preventDefault();

            let self = this;
            let url = new URL(self.getAttribute('href'), document.location);

            let target;
            let targetSelector = self.dataset.target;
            if (targetSelector) {
                target = document.querySelector(targetSelector);
            }
            else {
                target = self.closest('.partial-block');
            }

            let partialKey = target.dataset.partialKey;
            let partialMethod = target.dataset.partialMethod;

            url.searchParams.set(partialKey, 'true');

            if (partialMethod == 'append') {
                self.classList.add('loading');
            }
            else {
                let loading = document.createElementFromString(templates.loading());
                target.append(loading);
            }

            let xhr = new XMLHttpRequest();

            xhr.onreadystatechange = function() {
                if (xhr.readyState < 4) {
                    return;
                }

                if (xhr.status !== 200) {
                    apiErrorCallback(xhr);
                    return;
                }

                if (partialMethod == 'append') {
                    if (xhr.responseText) {
                        self.remove();

                        let div = document.createElement('DIV');
                        div.innerHTML = xhr.responseText;
                        target.append(div);
                    }
                    else {
                        self.classList.remove('loading');
                    }
                }
                else if (xhr.responseText) {
                    target.innerHTML = xhr.responseText;
                }
                else {
                    loading.remove();
                }

                // Scroll to target
                let scrollable = getScrollable(target);
                if (scrollable) {
                    let paddingTop = getStylePropertyValue(scrollable, 'padding-top', true);
                    scrollable.scrollTo({top: target.offsetTop - paddingTop - 20, behaviour: 'smooth'});
                }

                // Trigger «load» event
                target.dispatchEvent(new Event('load'));
            };

            xhr.open('GET', url);
            xhr.send();
        };
    });
}


/*
 * Notifications
 */
const notify = {
    error: console.error,
    info: console.info,
    success: console.info,
    warning: console.warn,
};


/*
 * Global initialization
 */

/* Handlebars templates */
document.querySelectorAll('script[type="text/x-handlebars-template"]').forEach(element => {
    templates[toCamelCase(element.id.replace('tpl-', ''))] = Handlebars.compile(element.innerHTML);
});

/* Handle partial blocks */
partialBlockSetup();

document.querySelectorAll('div.partial-block').forEach(element => {
    element.addEventListener('load', _e => {
        partialBlockSetup(element);
    });
});

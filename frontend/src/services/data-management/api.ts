import {request} from "@@/plugin-request/request";

export const getColumnsList = async (modelName: string) =>
  request(`/dashboard/api/v2/get_columns/${modelName}`, {
    method: 'GET',
  });

export const getFormDataJson = async (modelName: string, id_: string) =>
  request(`/dashboard/api/v2/get_form_data/${modelName}/${id_}`, {
    method: 'GET',
  });

export const postFormDataJson = async (modelName: string, id_: string) =>
  request(`/dashboard/api/v2/get_form_data/${modelName}/${id_}`, {
    method: 'POST',
  });

export const postEditedFormData = async (modelName: string, id_: string, body: any) =>
  request(`/dashboard/api/v2/edit_form_data`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    data: {'data': body, 'model': modelName, 'id_': id_},
  });

export const getTableData = async (modelName: string, body: any) =>
  request(`/dashboard/api/v2/get_table_data`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    data: {...body, 'model': modelName},
  });

// export const getTableData = async (modelName: string, body: any) =>
//   request(`/dashboard/api/v2/get_table_data`, {
//     method: 'POST',
//     headers: {
//       'Content-Type': 'application/json',
//     },
//     data: {...body, 'model': modelName},
//   });


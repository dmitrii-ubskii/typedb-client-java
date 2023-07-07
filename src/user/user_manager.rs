/*
 * Copyright (C) 2022 Vaticle
 *
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */

use std::future::Future;

use crate::{common::Result, connection::ServerConnection, error::ConnectionError, Connection, User};

#[derive(Clone, Debug)]
pub struct UserManager {
    connection: Connection,
}

impl UserManager {
    pub fn new(connection: Connection) -> Self {
        Self { connection }
    }

    pub async fn current_user(&self) -> Result<Option<User>> {
        match self.connection.username() {
            Some(username) => self.get(username.to_owned()).await,
            None => Ok(None),
        }
    }

    pub async fn all(&self) -> Result<Vec<User>> {
        self.run_any_node(|server_connection: ServerConnection| async move { server_connection.all_users().await })
            .await
    }

    pub async fn contains(&self, username: String) -> Result<bool> {
        self.run_any_node(|server_connection: ServerConnection| {
            let username = username.clone();
            async move { server_connection.contains_user(username).await }
        })
        .await
    }

    pub async fn create(&self, username: String, password: String) -> Result {
        self.run_any_node(|server_connection: ServerConnection| {
            let username = username.clone();
            let password = password.clone();
            async move { server_connection.create_user(username, password).await }
        })
        .await
    }

    pub async fn delete(&self, username: String) -> Result {
        self.run_any_node(|server_connection: ServerConnection| {
            let username = username.clone();
            async move { server_connection.delete_user(username).await }
        })
        .await
    }

    pub async fn get(&self, username: String) -> Result<Option<User>> {
        self.run_any_node(|server_connection: ServerConnection| {
            let username = username.clone();
            async move { server_connection.get_user(username).await }
        })
        .await
    }

    pub async fn set_password(&self, username: String, password: String) -> Result {
        self.run_any_node(|server_connection: ServerConnection| {
            let username = username.clone();
            let password = password.clone();
            async move { server_connection.set_user_password(username, password).await }
        })
        .await
    }

    async fn run_any_node<F, P, R>(&self, task: F) -> Result<R>
    where
        F: Fn(ServerConnection) -> P,
        P: Future<Output = Result<R>>,
    {
        let mut error_buffer = Vec::with_capacity(self.connection.server_count());
        for server_connection in self.connection.connections() {
            match task(server_connection.clone()).await {
                Ok(res) => {
                    return Ok(res);
                }
                Err(err) => error_buffer.push(format!("- {}: {}", server_connection.address(), err)),
            }
        }
        Err(ConnectionError::ClusterAllNodesFailed(error_buffer.join("\n")))?
    }
}

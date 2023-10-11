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

use std::sync::Arc;

use typeql::pattern::{Conjunction, Variable};

use crate::{
    common::{stream::Stream, Result},
    connection::TransactionStream,
    logic::Rule,
};

/// Provides methods for manipulating rules in the database.
#[derive(Clone, Debug)]
pub struct LogicManager {
    pub(super) transaction_stream: Arc<TransactionStream>,
}

impl LogicManager {
    pub(crate) fn new(transaction_stream: Arc<TransactionStream>) -> Self {
        Self { transaction_stream }
    }

    /// Creates a new Rule if none exists with the given label, or replaces the existing one.
    ///
    /// # Arguments
    ///
    /// * `label` -- The label of the Rule to create or replace
    /// * `when` -- The when body of the rule to create
    /// * `then` -- The then body of the rule to create
    ///
    /// # Examples
    ///
    /// ```rust
    #[cfg_attr(feature = "sync", doc = "transaction.logic().put_rule(label, when, then)")]
    #[cfg_attr(not(feature = "sync"), doc = "transaction.logic().put_rule(label, when, then).await")]
    /// ```
    #[cfg_attr(feature = "sync", maybe_async::must_be_sync)]
    pub async fn put_rule(&self, label: String, when: Conjunction, then: Variable) -> Result<Rule> {
        self.transaction_stream.put_rule(label, when, then).await
    }

    /// Retrieves the Rule that has the given label.
    ///
    /// # Arguments
    ///
    /// * `label` -- The label of the Rule to create or retrieve
    ///
    /// # Examples
    ///
    /// ```rust
    #[cfg_attr(feature = "sync", doc = "transaction.logic().get_rule(label)")]
    #[cfg_attr(not(feature = "sync"), doc = "transaction.logic().get_rule(label).await")]
    /// ```
    #[cfg_attr(feature = "sync", maybe_async::must_be_sync)]
    pub async fn get_rule(&self, label: String) -> Result<Option<Rule>> {
        self.transaction_stream.get_rule(label).await
    }

    /// Retrieves all rules.
    ///
    /// # Examples
    ///
    /// ```rust
    /// transaction.logic.get_rules()
    /// ```
    pub fn get_rules(&self) -> Result<impl Stream<Item = Result<Rule>>> {
        self.transaction_stream.get_rules()
    }
}

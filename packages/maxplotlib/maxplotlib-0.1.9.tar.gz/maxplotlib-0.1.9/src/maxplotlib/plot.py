from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
import torch


def multi_hist(
    df,
    x_col,
    y_labels,
    x_label=None,
    title=None
) -> None:
    """Plots a histogram with multiple groups
    
    Args:
        df: data
        x_col: column of variable whose frequency we are plotting
        y_labels: label for each group
        x_label: label for x axis
        title: title

    """
    fig, ax = plt.subplots(1, 2, figsize=(10, 5))
    fig.suptitle(title, fontsize=15)
    assert 'label' in df and x_col in df
    colors = ['blue', 'green', 'yellow', 'red', 'orange', 'purple', 'pink', 'brown', 'grey', 'black']
    for k in range(2):
        for i in range(len(y_labels)):
            subdf = df[df['label'] == i]
            ax[k].hist(
                subdf[x_col], 
                bins=20, 
                color=colors[i], 
                alpha=0.25, 
                label=y_labels[i]
            )
        ax[k].set_xlabel(x_label)
        ax[k].set_ylabel('Frequency')
        ax[k].set_xlim([1, df[x_col].max()])
        ax[k].legend()
    ax[0].set_title("linear scale")
    ax[1].set_xscale("log")
    ax[1].set_title("log scale")
    plt.tight_layout()
    plt.show()


def multi_logreg(
    lr,
    X,
    Y,
    X_axis_label=None,
    y_labels=None,
    title=None
) -> None:
    """Plots the predictions of a logistic regression model with 1-dimensional input and N-dimensional output

    Plots in both linear and logarithmic view

    Args
        lr: sklearn logistic regression model
        X: (n_data,) List[Union[int,float]] input predictors
        Y: (n_data,) List[int] output labels
        X_axis_label: str
        y_labels: List[str]
        title: str
    """
    fig, ax = plt.subplots(1, 2, figsize=(10,5), sharey=True)

    colors = ['blue', 'green', 'yellow', 'red', 'orange', 'purple', 'pink', 'brown', 'grey', 'black']

    # plot data by predictor along X axis and class label along the Y axis
    for i in range(2):
        ax[i].scatter(
            X, 
            max(Y) - Y, 
            sizes = 5*np.ones(len(X)), 
            label=X_axis_label
        )

    # plot logistic regression model predictions
    xplot = np.arange(0,max(X),.1)
    plotpreds = max(Y) - lr.predict(xplot.reshape(-1,1))
    for i in range(2):
        ax[i].plot(
            xplot, 
            plotpreds, 
            linewidth=12.5, 
            color='grey', 
            alpha=0.5, 
            label = "LogReg Prediction", 
            linestyle=':'
        )

    # fill a region of space whose width changes proportional to the predicted probabiltiy of the LR model for each class
    probs = lr.predict_proba(xplot.reshape(-1,1))
    for i in range(2):
        for j, y_label in enumerate(y_labels):
            ax[i].fill_between(
                xplot, 
                max(Y) - j - 0.5*probs[:,j], 
                max(Y) - j + 0.5*probs[:,j], 
                linewidth=5, 
                color=colors[j], 
                alpha=0.3, 
                label=f'LogReg P({y_label})'
            )

    fig.suptitle(title)
    for i in range(2):
        x_ticks = list(range(10, max(X), 10))
        y_ticks = np.arange(0,len(set(Y)) - 0.5, 0.5)
        ax[i].set_xlim([.5,max(X)])
        ax[i].set_xticks(x_ticks)
        ax[i].set_xticklabels([str(x) for x in x_ticks], fontsize=5)
        ax[i].set_yticks(y_ticks)
        ax[i].set_yticklabels([label for y in y_labels[::-1] for label in (y, '')][:-1])
        ax[i].set_xlabel(X_axis_label)
        ax[i].legend(loc='lower right')
    
    ax[0].set_title('linear scale')
    ax[1].set_title('log scale')
    ax[1].set_xscale('log')
    plt.tight_layout()


def plot_embedding_trajectories(
    embeddings, 
    labels, 
    title=None,
) -> None:
    """Plots a trajectory for each GNN node's embedding during training
    
    Args:
        embeddings: (n_epochs, n_data, 2)
        labels: (n_data,)
    """
    epochs, nodes, dimensions = embeddings.shape
    assert dimensions == 2, "The embeddings should be 2-dimensional."
    assert len(labels) == nodes, "The number of labels should match the number of nodes."
    colors = ['blue', 'green', 'yellow', 'red', 'orange', 'purple', 'pink', 'brown', 'grey', 'black']
    fig = go.Figure()
    for node_idx in range(nodes):
        label = labels[node_idx]
        fig.add_trace(
            go.Scatter3d(
                x=np.arange(epochs), 
                y=embeddings[:, node_idx, 0], 
                z=embeddings[:, node_idx, 1], 
                mode='lines',
                line=dict(color=colors[label], width=5),
                opacity=0.1
            )
        )
    fig.update_layout(
        title=title,
        autosize=False,
        width=1000,
        height=600,
        showlegend=False,
        scene=dict(
            xaxis=dict(title='Epochs',tickvals=[]),
            yaxis_title='Dim 1',
            zaxis_title='Dim 2',
            aspectmode='manual', aspectratio=dict(x=3, y=1, z=1),
            camera=dict(
                eye=dict(x=1, y=2, z=0.5)
            )
        ),
    )
    fig.show()
        

def plot_embedding_spaces(
    models, 
    modelnames
) -> None:
    """Plots the predictions of each model in a 2d embedding space

    Args:
        models: List[torch models]
        modelnames: List[str]
    """
    fig, ax = plt.subplots(1, len(models), figsize=(len(models)*4,4))

    colors = ['blue', 'green', 'yellow', 'red', 'orange', 'purple', 'pink', 'brown', 'grey', 'black']
    cmap = ListedColormap(colors[:4])
    x_min, x_max = -1, 1
    y_min, y_max = -1, 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.02), np.arange(y_min, y_max, 0.02))
    for i, model in enumerate(models):
        if len(models)==1:
            _ax = ax
        else:
            _ax = ax[i]
        assert model.classifier.in_features == 2
        name = modelnames[i]
        pred = model.classifier(torch.from_numpy(np.c_[xx.ravel(), yy.ravel()]).float()).detach().numpy()
        zz = np.argmax(pred, axis=1).reshape(xx.shape)
        _ax.pcolormesh(xx, yy, zz, cmap=cmap)
        _ax.set_title(name)
        _ax.set_xlabel('embedding dim 1')
        _ax.set_ylabel('embedding dim 2')
    plt.tight_layout()
    plt.show()    
        

def plot_training_results(
    losses, 
    acc, 
    modelnames
) -> None:
    """Plots the change in loss & accuracy for a set of models during training

    One model per row

    Args:
        losses: Dict[str -> List[float]], loss of each model during training
        acc: Dict[str -> List[float]], accuracy of each model during training
        modelnames: List[str]
    """
    assert list(losses.keys()) == modelnames and list(acc.keys()) == modelnames
    n_models = len(modelnames)
    fig, ax = plt.subplots(2, n_models, figsize=(3*n_models,6))
    if n_models == 1:
        model_acc = acc[modelnames[0]]
        ax[0].set_title(f'{modelnames[0]}: accuracy')
        ax[0].plot(np.arange(len(model_acc)), [x[0] for x in model_acc], label='train acc')
        ax[0].plot(np.arange(len(model_acc)), [x[1] for x in model_acc], label='test acc')
        ax[0].set_xlabel('# epochs')
        ax[0].set_xticks([])
        ax[0].legend(loc='lower right')
        ax[0].set_ylim(([0,1]))

        model_losses = losses[modelnames[0]]
        ax[1].set_title(f'{modelnames[0]}: loss')
        ax[1].plot(np.arange(len(model_losses)), model_losses)
        ax[1].set_xlabel('# epochs')
        ax[1].set_xticks([])
        ax[1].set_ylim(([0,max([max(losses[name]) for name in modelnames])]))
    else:
        for i in range(n_models):
            model_acc = acc[modelnames[i]]
            ax[0,i].set_title(f'{modelnames[i]}: accuracy')
            ax[0,i].plot(np.arange(len(model_acc)), [x[0] for x in model_acc], label='train acc')
            ax[0,i].plot(np.arange(len(model_acc)), [x[1] for x in model_acc], label='test acc')
            ax[0,i].set_xlabel('# epochs')
            ax[0,i].set_xticks([])
            ax[0,i].legend(loc='lower right')
            ax[0,i].set_ylim(([0,1]))

            model_losses = losses[modelnames[i]]
            ax[1,i].set_title(f'{modelnames[i]}: loss')
            ax[1,i].plot(np.arange(len(model_losses)), model_losses)
            ax[1,i].set_xlabel('# epochs')
            ax[1,i].set_xticks([])
            ax[1,i].set_ylim(([0,max([max(losses[name]) for name in modelnames])]))
    plt.tight_layout()
    

def plot_graph_geography(
    graph, 
    geodf, 
    title=None
) -> None:
    """Plots a NetworkX graph with nodes situated in their given latitude/longitude coordinates

    Args:
        graph: networkX graph
        geodf: pandas DataFrame with lat/lon coordinates of nodes in graph
            the index values of geodf should match the node values of graph
    """
    
    # gets latitude & longitude coords for each node by ID from geodf
    geo_df_row = lambda i : geodf.loc[geodf.index==i]
    
    # gets edge connections from graph of nodes in geodf
    connections = graph.subgraph(geodf.index).edges()
    
    node_ids = np.array(connections).flatten()
    
    connections_coords = np.array([[geo_df_row(i).lon, geo_df_row(i).lat] for i in node_ids]).reshape(len(node_ids), 2)

    fig = go.Figure(
        data=[
            go.Scattergeo(
                lon = connections_coords[:,0],
                lat = connections_coords[:,1],
                mode = 'lines',
                line=dict(
                    color='black', 
                    width=.03)
            ),
            go.Scattergeo(
                lon = geodf['lon'],
                lat = geodf['lat'],
                text = geodf['name'],
                mode = 'markers',
                hoverinfo='text'
            )
    ])  

    fig.update_geos(fitbounds='locations')
    if title: fig.update_layout(title=title, showlegend=False)
    fig.update_layout(
        autosize=False,
        width=1000,
        height=600,
    )
    fig.show()
